import asyncio
from asgiref.sync import sync_to_async
from pydantic import Field
import google.generativeai as genai
from pydantic.dataclasses import dataclass
from playwright.async_api import async_playwright
from django.conf import settings
from work_us import models as wk_models


@dataclass
class AttorneyOfficeAgent:
    """Request and query to attorney page"""

    id: int = Field(..., description="ID of the candidate")

    def __post_init__(self):
        candidate: wk_models.CandidateModel = wk_models.CandidateModel.objects.get(
            id=self.id
        )
        asyncio.run(self.run_query(candidate=candidate))

    async def __select_id_type(self, iframe, value: str):
        await iframe.select_option("select#ddlTipoID", value=value)

    async def __typing_id(self, iframe, value: str):
        """Fill the ID number"""
        await iframe.fill("#txtNumID", value)

    async def __typing_captcha(self, iframe, value: str):
        """Fill the captcha answer"""
        await iframe.fill("#txtRespuestaPregunta", value)

    async def __captcha_solver(self, iframe, query: str, id: str, name: str):
        """Solve the captcha using the llm"""
        prompt: str = f"""
            Estoy consultando en la página de la Procuraduría General de la Nación de Colombia
            antecedentes de {name} con cédula {id}.
            Necesito responder la siguiente pregunta, responde únicamente cómo se especifica:
            {query}
        """
        genai.configure(api_key=settings.GEMINI_API_KEY)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    async def __process_content(self, content: str, id: str, name: str):
        """Process the content of the page"""
        # Aquí puedes agregar el código para procesar el contenido
        # Por ejemplo, extraer información específica del HTML
        prompt: str = f"""
            En esta página de la Procuraduría General de la Nación de Colombia busca todo lo relacionado
            con el usuario {name} con cédula {id}.
            El contenido de la página es el siguiente:
            {content}

            Genera un informe en formato de texto plano con la información sobre los antecedentes.
            Dame qué antecedentes tiene y una breve descripción de cada uno.
            Si no hay antecedentes, responde "No hay antecedentes".
            No me des ningún otro tipo de información, solo el informe.
        """
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text.strip()

    async def run_query(self, candidate: wk_models.CandidateModel):
        """Main function to the run agent"""
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                locale="es-CO",  # Colombian Spanish locale
                timezone_id="America/Bogota",
            )
            page = await context.new_page()

            # Extra permissions and flags
            await context.grant_permissions(["geolocation"])
            await page.set_extra_http_headers(
                {
                    "Accept-Language": "es-CO,es;q=0.9",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
                    "Connection": "keep-alive",
                }
            )
            await page.goto(
                "https://www.procuraduria.gov.co/Pages/Consulta-de-Antecedentes.aspx",
                wait_until="load",
            )

            # Esperar y acceder al iframe
            iframe_element = await page.wait_for_selector("iframe", timeout=10000)
            iframe = await iframe_element.content_frame()

            if not iframe:
                raise Exception("No se pudo acceder al iframe del formulario")

            # Fill the information
            await self.__select_id_type(iframe, "1")
            await self.__typing_id(iframe, candidate.number_id)

            # Get the captcha question
            captcha_text = await iframe.inner_text("#lblPregunta")
            print(f"Captcha question: {captcha_text}", flush=True)
            solve = await self.__captcha_solver(
                iframe, captcha_text, candidate.number_id, candidate.name
            )
            print(f"Captcha answer: {solve}", flush=True)

            # Fill the captcha answer
            await self.__typing_captcha(iframe, solve)

            # Aquí falta código para hacer clic en el botón de consulta
            await iframe.click("#btnConsultar")
            await page.wait_for_timeout(5000)

            # All content of the page
            content = await iframe.content()
            result = await self.__process_content(
                content, candidate.number_id, candidate.name
            )
            print(f"Result of the query: {result}", flush=True)

            # Create the background in the database
            await self.save_background(candidate=candidate, result=result)

            # Cerrar el navegador
            await browser.close()

    @sync_to_async
    def save_background(self, candidate: wk_models.CandidateModel, result: str):
        """Save the background in the database"""
        wk_models.BackgroundPersonModel.objects.create(
            candidate=candidate,
            organization=wk_models.BackgroundPersonModel.OrganizationType.ATTORNEY,
            query=result,
        )
