from aiohttp.web import Response
from aiohttp.web import View

from aiohttp_jinja2 import render_template

from lib.image import image_to_img_src
from lib.image import PolygonDrawer
from lib.image import open_image


class IndexView(View):
    template = "index.html"

    async def get(self) -> Response:
        ctx = {}
        return render_template(self.template, self.request, ctx)

    async def post(self) -> Response:
        try:
            form = await self.request.post()
            image = open_image(form["image"].file)
            draw = PolygonDrawer(image)
            model = self.request.app["model"]
            words = []
            results = model(image)
            for result in results:
                for idx, _ in enumerate(result.boxes.data):
                    coords, word, accuracy = (result.boxes.data[idx][:4]).cpu().numpy(), result.names[result.boxes.data[idx][-1].cpu().item()], (result.boxes.data[idx][[-2]]).cpu().item()

                    if accuracy <= 0.5:
                        continue

                    draw.highlight_word(coords, word)
                    cropped_img = draw.crop(coords)
                    cropped_img_b64 = image_to_img_src(cropped_img)
                    words.append(
                        {
                            "image": cropped_img_b64,
                            "word": word,
                            "accuracy": accuracy,
                        }
                    )
            image_b64 = image_to_img_src(draw.get_highlighted_image())
            ctx = {"image": image_b64, "words": words}
        except Exception as err:
            ctx = {"error": str(err)}
        return render_template(self.template, self.request, ctx)