

import segno
from urllib.request import urlopen

slts_qrcode = segno.make_qr("https://youtu.be/dQw4w9WgXcQ")
#nirvana_url = urlopen("https://media.giphy.com/media/LpwBqCorPvZC0/giphy.gif")
slts_qrcode.to_artistic(
    background="rick-rolling.gif",
    target="animated_qrcode.gif",
    scale=20,
)