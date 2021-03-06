import aiohttp
import asyncio
import uvicorn
from fastai import *
from fastai.vision import *
from io import BytesIO
from starlette.applications import Starlette
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

export_file_url = 'https://www.dropbox.com/s/9gu51wf4zuq7qk4/export.pkl?dl=1'
export_file_name = 'export.pkl'

classes = ['AFRICAN FIREFINCH',
 'ALBATROSS',
 'ALEXANDRINE PARAKEET',
 'AMERICAN AVOCET',
 'AMERICAN BITTERN',
 'AMERICAN COOT',
 'AMERICAN GOLDFINCH',
 'AMERICAN KESTREL',
 'AMERICAN PIPIT',
 'AMERICAN REDSTART',
 'ANHINGA',
 'ANNAS HUMMINGBIRD',
 'ANTBIRD',
 'ARARIPE MANAKIN',
 'BALD EAGLE',
 'BALTIMORE ORIOLE',
 'BANANAQUIT',
 'BAR-TAILED GODWIT',
 'BARN OWL',
 'BARN SWALLOW',
 'BAY-BREASTED WARBLER',
 'BEARDED BARBET',
 'BELTED KINGFISHER',
 'BIRD OF PARADISE',
 'BLACK FRANCOLIN',
 'BLACK SKIMMER',
 'BLACK SWAN',
 'BLACK THROATED WARBLER',
 'BLACK VULTURE',
 'BLACK-CAPPED CHICKADEE',
 'BLACK-NECKED GREBE',
 'BLACK-THROATED SPARROW',
 'BLACKBURNIAM WARBLER',
 'BLUE GROUSE',
 'BLUE HERON',
 'BOBOLINK',
 'BROWN NOODY',
 'BROWN THRASHER',
 'CACTUS WREN',
 'CALIFORNIA CONDOR',
 'CALIFORNIA GULL',
 'CALIFORNIA QUAIL',
 'CANARY',
 'CAPE MAY WARBLER',
 'CAPUCHINBIRD',
 'CARMINE BEE-EATER',
 'CASPIAN TERN',
 'CASSOWARY',
 'CHARA DE COLLAR',
 'CHIPPING SPARROW',
 'CINNAMON TEAL',
 'COCK OF THE  ROCK',
 'COCKATOO',
 'COMMON GRACKLE',
 'COMMON HOUSE MARTIN',
 'COMMON LOON',
 'COMMON POORWILL',
 'COMMON STARLING',
 'COUCHS KINGBIRD',
 'CRESTED AUKLET',
 'CRESTED CARACARA',
 'CROW',
 'CROWNED PIGEON',
 'CUBAN TODY',
 'CURL CRESTED ARACURI',
 'D-ARNAUDS BARBET',
 'DARK EYED JUNCO',
 'DOWNY WOODPECKER',
 'EASTERN BLUEBIRD',
 'EASTERN MEADOWLARK',
 'EASTERN ROSELLA',
 'EASTERN TOWEE',
 'ELEGANT TROGON',
 'ELLIOTS  PHEASANT',
 'EMPEROR PENGUIN',
 'EMU',
 'EURASIAN MAGPIE',
 'EVENING GROSBEAK',
 'FLAME TANAGER',
 'FLAMINGO',
 'FRIGATE',
 'GILA WOODPECKER',
 'GILDED FLICKER',
 'GLOSSY IBIS',
 'GOLD WING WARBLER',
 'GOLDEN CHEEKED WARBLER',
 'GOLDEN CHLOROPHONIA',
 'GOLDEN EAGLE',
 'GOLDEN PHEASANT',
 'GOULDIAN FINCH',
 'GRAY CATBIRD',
 'GRAY PARTRIDGE',
 'GREEN JAY',
 'GREY PLOVER',
 'GUINEAFOWL',
 'HAWAIIAN GOOSE',
 'HOODED MERGANSER',
 'HOOPOES',
 'HORNBILL',
 'HOUSE FINCH',
 'HOUSE SPARROW',
 'HYACINTH MACAW',
 'IMPERIAL SHAQ',
 'INCA TERN',
 'INDIGO BUNTING',
 'JABIRU',
 'JAVAN MAGPIE',
 'KILLDEAR',
 'KING VULTURE',
 'LARK BUNTING',
 'LILAC ROLLER',
 'LONG-EARED OWL',
 'MALACHITE KINGFISHER',
 'MALEO',
 'MALLARD DUCK',
 'MANDRIN DUCK',
 'MARABOU STORK',
 'MASKED BOOBY',
 'MIKADO  PHEASANT',
 'MOURNING DOVE',
 'MYNA',
 'NICOBAR PIGEON',
 'NORTHERN CARDINAL',
 'NORTHERN FLICKER',
 'NORTHERN GANNET',
 'NORTHERN GOSHAWK',
 'NORTHERN JACANA',
 'NORTHERN MOCKINGBIRD',
 'NORTHERN PARULA',
 'NORTHERN RED BISHOP',
 'OCELLATED TURKEY',
 'OSPREY',
 'OSTRICH',
 'PAINTED BUNTIG',
 'PARADISE TANAGER',
 'PARUS MAJOR',
 'PEACOCK',
 'PELICAN',
 'PEREGRINE FALCON',
 'PINK ROBIN',
 'PUFFIN',
 'PURPLE FINCH',
 'PURPLE GALLINULE',
 'PURPLE MARTIN',
 'PURPLE SWAMPHEN',
 'QUETZAL',
 'RAINBOW LORIKEET',
 'RAZORBILL',
 'RED FACED CORMORANT',
 'RED FACED WARBLER',
 'RED HEADED DUCK',
 'RED HEADED WOODPECKER',
 'RED HONEY CREEPER',
 'RED THROATED BEE EATER',
 'RED WINGED BLACKBIRD',
 'RED WISKERED BULBUL',
 'RING-BILLED GULL',
 'RING-NECKED PHEASANT',
 'ROADRUNNER',
 'ROBIN',
 'ROCK DOVE',
 'ROSY FACED LOVEBIRD',
 'ROUGH LEG BUZZARD',
 'RUBY THROATED HUMMINGBIRD',
 'RUFOUS KINGFISHER',
 'RUFUOS MOTMOT',
 'SAND MARTIN',
 'SCARLET IBIS',
 'SCARLET MACAW',
 'SHOEBILL',
 'SNOWY EGRET',
 'SNOWY OWL',
 'SORA',
 'SPANGLED COTINGA',
 'SPLENDID WREN',
 'SPOONBILL',
 'STEAMER DUCK',
 'STORK BILLED KINGFISHER',
 'STRAWBERRY FINCH',
 'TAIWAN MAGPIE',
 'TEAL DUCK',
 'TIT MOUSE',
 'TOUCHAN',
 'TOWNSENDS WARBLER',
 'TREE SWALLOW', 'TRUMPTER SWAN', 'TURKEY VULTURE', 'TURQUOISE MOTMOT', 'VARIED THRUSH', 'VENEZUELIAN TROUPIAL', 'VERMILION FLYCATHER', 'VIOLET GREEN SWALLOW', 'WATTLED CURASSOW', 'WHITE CHEEKED TURACO', 'WHITE NECKED RAVEN', 'WHITE TAILED TROPIC', 'WILD TURKEY', 'WILSONS BIRD OF PARADISE', 'WOOD DUCK', 'YELLOW HEADED BLACKBIRD']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))


async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise


loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()


@app.route('/')
async def homepage(request):
    html_file = path / 'view' / 'index.html'
    return HTMLResponse(html_file.open().read())


@app.route('/analyze', methods=['POST'])
async def analyze(request):
    img_data = await request.form()
    img_bytes = await (img_data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({'result': str(prediction)})


if __name__ == '__main__':
    if 'serve' in sys.argv:
        uvicorn.run(app=app, host='0.0.0.0', port=5000, log_level="info")
