from PIL import Image, ImageFont, ImageDraw
import qrcode

def generate_label(uid: str, name: str, probe_type: str) -> str:
    img = Image.open("blank_label.png")
    font = ImageFont.truetype("Roboto-Medium.ttf", 69)
    x_max = max(max(font.getlength(f"UID: {uid}"), font.getlength(f"Тип пробы: {probe_type}")),
                font.getlength(f"Дрон с пробой был принят: {name}")) + 200 + 100
    qr = qrcode.make(f"https://t.me/siburopenecomapbot?start={uid.replace('-', 'X')}")
    qr = qr.resize((225, 225))
    img.paste(qr, (0, 225))
    imgDraw = ImageDraw.Draw(img)
    imgDraw.text((225+50, 75), f"UID: {uid}", (0, 0, 0), font, "lm")
    imgDraw.text((225+50, 225), f"Дрон с пробой был принят: {name}", (0, 0, 0), font, "lm")
    imgDraw.text((225+50, 375), f"Тип пробы: {probe_type}", (0, 0, 0), font, "lm")
    img = img.crop((0, 0, x_max, 450))
    img.save(f"label_{id(img)}.png")
    return f"label_{id(img)}.png"

if __name__ == "__main__":
    generate_label("157393fe-7f1f-4a2c-9594-1a21377c8865", "Брагинец П. В.")