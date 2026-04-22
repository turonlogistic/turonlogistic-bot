#!/usr/bin/env python3
"""
Turon Logistic Group — Telegram Bot
Языки: RU / UZ / EN
Менеджер: @TLG_UZB
"""

import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

TOKEN = "8608657013:AAHxDm7XXlUc8tcRwAL8kFqdYZqwa8NuJ0M"

logging.basicConfig(level=logging.INFO)

LANG, MENU, FROM_WHERE, TO_WHERE, CARGO_TYPE, TRANSPORT, WEIGHT, DIMENSIONS, STACKABLE, CONTACT = range(10)

T = {
    "ru": {
        "welcome": "👋 Добро пожаловать в <b>Turon Logistic Group</b>!\n\n🚚 Международные грузоперевозки и таможенное оформление.\nЕвропа • Китай • Турция → Узбекистан\n\nВыберите действие:",
        "menu": ["📦 Оставить заявку", "📞 Контакты", "ℹ️ О компании"],
        "ask_from": "📍 Откуда нужно доставить груз?\n(Например: Шанхай, Китай)",
        "ask_to": "📍 Куда доставить?\n(Например: Ташкент, Узбекистан)",
        "ask_cargo": "📦 Что везём? Опишите товар:",
        "ask_transport": "🚛 Выберите вид транспорта:",
        "transport_opts": ["🚛 Авто", "🚂 Железная дорога", "✈️ Авиа", "📦 Сборный груз", "❓ Не знаю / Посоветуйте"],
        "ask_weight": "⚖️ Примерный вес и объём груза?\n(Например: 500 кг, 2 куб.м)",
        "ask_dimensions": "📐 Размеры одного места (упаковки)?\n(Например: 120х80х100 см или напишите 'не знаю')",
        "ask_stackable": "📦 Можно ли штабелировать груз?\n(Ставить ящики/паллеты друг на друга)",
        "stackable_opts": ["✅ Да, можно", "❌ Нет, нельзя", "⚠️ Только 1 ярус", "❓ Не знаю"],
        "ask_contact": "📱 Ваш номер телефона или Telegram для связи:",
        "done": "✅ <b>Заявка принята!</b>\n\nНаш менеджер свяжется с вами в ближайшее время.\nОбычно отвечаем в течение 30 минут в рабочее время.\n\nСпасибо, что выбрали Turon Logistic Group! 🙏",
        "contacts": "📞 <b>Контакты Turon Logistic Group</b>\n\n📱 Телефон: +998 95 341 05 50\n✉️ Email: info@turonlogistic.uz\n📍 Адрес: г. Ташкент, ул. А.Темура, 1 проезд, дом 6\n🌐 Сайт: turonlogistic.uz\n✈️ Telegram-канал: @pro_customsuz",
        "about": "🏢 <b>О компании Turon Logistic Group</b>\n\n✅ 10 лет на рынке\n✅ Доставка из Европы, Китая, Турции\n✅ Все виды транспорта: авто, ж/д, авиа\n✅ Таможенное оформление под ключ\n✅ Сборные грузы — экономия до 60%\n✅ Поиск производителей\n\nПрофессионально. Надёжно. В срок.",
        "notify": "🔔 <b>НОВАЯ ЗАЯВКА</b>\n\n🌍 Откуда: {a}\n📍 Куда: {b}\n📦 Товар: {c}\n🚛 Транспорт: {d}\n⚖️ Вес/объём: {e}\n📐 Размеры: {f}\n📦 Штабелирование: {g}\n📱 Контакт: {h}\n👤 Telegram: {i}\n🌐 Язык: RU",
    },
    "uz": {
        "welcome": "👋 <b>Turon Logistic Group</b>ga xush kelibsiz!\n\n🚚 Xalqaro yuk tashish va bojxona rasmiylashtiruvi.\nYevropa • Xitoy • Turkiya → O'zbekiston\n\nAmalni tanlang:",
        "menu": ["📦 Ariza qoldirish", "📞 Aloqa", "ℹ️ Kompaniya haqida"],
        "ask_from": "📍 Yuk qayerdan olib kelinadi?\n(Masalan: Shanxay, Xitoy)",
        "ask_to": "📍 Qayerga yetkazish kerak?\n(Masalan: Toshkent, O'zbekiston)",
        "ask_cargo": "📦 Nima olib kelamiz? Tovarni tasvirlang:",
        "ask_transport": "🚛 Transport turini tanlang:",
        "transport_opts": ["🚛 Avto", "🚂 Temir yo'l", "✈️ Avia", "📦 Yig'ma yuk", "❓ Bilmayman / Maslahat bering"],
        "ask_weight": "⚖️ Taxminiy og'irlik va hajm?\n(Masalan: 500 kg, 2 kub.m)",
        "ask_dimensions": "📐 Bir o'rin o'lchamlari?\n(Masalan: 120x80x100 sm yoki 'bilmayman' deb yozing)",
        "ask_stackable": "📦 Yukni shtabellashtirish mumkinmi?",
        "stackable_opts": ["✅ Ha, mumkin", "❌ Yo'q, mumkin emas", "⚠️ Faqat 1 qator", "❓ Bilmayman"],
        "ask_contact": "📱 Telefon raqamingiz yoki Telegram:",
        "done": "✅ <b>Ariza qabul qilindi!</b>\n\nMenejerimiz tez orada siz bilan bog'lanadi.\n\nTuron Logistic Group'ni tanlaganingiz uchun rahmat! 🙏",
        "contacts": "📞 <b>Turon Logistic Group</b>\n\n📱 Telefon: +998 95 341 05 50\n✉️ Email: info@turonlogistic.uz\n📍 Toshkent sh., A.Temur ko'chasi, 1-o'tish, 6-uy\n🌐 turonlogistic.uz\n✈️ @pro_customsuz",
        "about": "🏢 <b>Turon Logistic Group</b>\n\n✅ Bozorda 10 yil\n✅ Yevropa, Xitoy, Turkiyadan yetkazib berish\n✅ Barcha transport turlari\n✅ Bojxona rasmiylashtiruvi\n✅ Yig'ma yuklar — 60% gacha tejash\n\nProfessional. Ishonchli. O'z vaqtida.",
        "notify": "🔔 <b>YANGI ARIZA</b>\n\n🌍 Qayerdan: {a}\n📍 Qayerga: {b}\n📦 Tovar: {c}\n🚛 Transport: {d}\n⚖️ Og'irlik: {e}\n📐 O'lchamlar: {f}\n📦 Shtabellash: {g}\n📱 Kontakt: {h}\n👤 Telegram: {i}\n🌐 Til: UZ",
    },
    "en": {
        "welcome": "👋 Welcome to <b>Turon Logistic Group</b>!\n\n🚚 International freight & customs clearance.\nEurope • China • Turkey → Uzbekistan\n\nChoose an option:",
        "menu": ["📦 Submit Request", "📞 Contacts", "ℹ️ About Us"],
        "ask_from": "📍 Where to pick up the cargo?\n(e.g. Shanghai, China)",
        "ask_to": "📍 Where to deliver?\n(e.g. Tashkent, Uzbekistan)",
        "ask_cargo": "📦 What are we shipping? Describe the goods:",
        "ask_transport": "🚛 Choose transport type:",
        "transport_opts": ["🚛 Road", "🚂 Railway", "✈️ Air", "📦 Groupage", "❓ Not sure / Advise me"],
        "ask_weight": "⚖️ Approximate weight and volume?\n(e.g. 500 kg, 2 cbm)",
        "ask_dimensions": "📐 Dimensions of one package?\n(e.g. 120x80x100 cm or type 'unknown')",
        "ask_stackable": "📦 Can the cargo be stacked?",
        "stackable_opts": ["✅ Yes, stackable", "❌ No, not stackable", "⚠️ 1 layer only", "❓ Unknown"],
        "ask_contact": "📱 Your phone number or Telegram:",
        "done": "✅ <b>Request received!</b>\n\nOur manager will contact you shortly.\n\nThank you for choosing Turon Logistic Group! 🙏",
        "contacts": "📞 <b>Turon Logistic Group</b>\n\n📱 Phone: +998 95 341 05 50\n✉️ Email: info@turonlogistic.uz\n📍 Tashkent, A.Temur St., 1st passage, 6\n🌐 turonlogistic.uz\n✈️ @pro_customsuz",
        "about": "🏢 <b>Turon Logistic Group</b>\n\n✅ 10 years in business\n✅ Europe, China, Turkey delivery\n✅ All transport modes\n✅ Full customs clearance\n✅ Groupage — save up to 60%\n\nProfessional. Reliable. On time.",
        "notify": "🔔 <b>NEW REQUEST</b>\n\n🌍 From: {a}\n📍 To: {b}\n📦 Cargo: {c}\n🚛 Transport: {d}\n⚖️ Weight: {e}\n📐 Dimensions: {f}\n📦 Stackable: {g}\n📱 Contact: {h}\n👤 Telegram: {i}\n🌐 EN",
    }
}

def lang_kb():
    return ReplyKeyboardMarkup([["🇷🇺 Русский", "🇺🇿 O'zbek", "🇬🇧 English"]], resize_keyboard=True, one_time_keyboard=True)

def menu_kb(lang):
    return ReplyKeyboardMarkup([[b] for b in T[lang]["menu"]], resize_keyboard=True)

def opts_kb(lang, key):
    return ReplyKeyboardMarkup([[o] for o in T[lang][key]], resize_keyboard=True, one_time_keyboard=True)

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data.clear()
    await update.message.reply_text("🌐 Выберите язык / Tilni tanlang / Choose language:", reply_markup=lang_kb())
    return LANG

async def set_lang(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    t = update.message.text
    lang = "uz" if "zbek" in t else ("en" if "nglish" in t else "ru")
    ctx.user_data["lang"] = lang
    await update.message.reply_text(T[lang]["welcome"], parse_mode="HTML", reply_markup=menu_kb(lang))
    return MENU

async def menu_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    text = update.message.text
    menu = T[lang]["menu"]
    if text == menu[0]:
        await update.message.reply_text(T[lang]["ask_from"], reply_markup=ReplyKeyboardRemove())
        return FROM_WHERE
    elif text == menu[1]:
        await update.message.reply_text(T[lang]["contacts"], parse_mode="HTML", reply_markup=menu_kb(lang))
    elif text == menu[2]:
        await update.message.reply_text(T[lang]["about"], parse_mode="HTML", reply_markup=menu_kb(lang))
    else:
        await update.message.reply_text(T[lang]["welcome"], parse_mode="HTML", reply_markup=menu_kb(lang))
    return MENU

async def get_from(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    ctx.user_data["a"] = update.message.text
    await update.message.reply_text(T[lang]["ask_to"])
    return TO_WHERE

async def get_to(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    ctx.user_data["b"] = update.message.text
    await update.message.reply_text(T[lang]["ask_cargo"])
    return CARGO_TYPE

async def get_cargo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    ctx.user_data["c"] = update.message.text
    await update.message.reply_text(T[lang]["ask_transport"], reply_markup=opts_kb(lang, "transport_opts"))
    return TRANSPORT

async def get_transport(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    ctx.user_data["d"] = update.message.text
    await update.message.reply_text(T[lang]["ask_weight"], reply_markup=ReplyKeyboardRemove())
    return WEIGHT

async def get_weight(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    ctx.user_data["e"] = update.message.text
    await update.message.reply_text(T[lang]["ask_dimensions"])
    return DIMENSIONS

async def get_dimensions(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    ctx.user_data["f"] = update.message.text
    await update.message.reply_text(T[lang]["ask_stackable"], reply_markup=opts_kb(lang, "stackable_opts"))
    return STACKABLE

async def get_stackable(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    ctx.user_data["g"] = update.message.text
    await update.message.reply_text(T[lang]["ask_contact"], reply_markup=ReplyKeyboardRemove())
    return CONTACT

async def get_contact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    d = ctx.user_data
    d["h"] = update.message.text
    d["i"] = f"@{update.message.from_user.username}" if update.message.from_user.username else f"ID:{update.message.chat_id}"

    msg = T[lang]["notify"].format(
        a=d.get("a","—"), b=d.get("b","—"), c=d.get("c","—"),
        d=d.get("d","—"), e=d.get("e","—"), f=d.get("f","—"),
        g=d.get("g","—"), h=d.get("h","—"), i=d.get("i","—")
    )

    try:
        await ctx.bot.send_message(chat_id=7729758589, text=msg, parse_mode="HTML")
    except Exception as e:
        logging.warning(f"Ошибка отправки менеджеру: {e}")

    await update.message.reply_text(T[lang]["done"], parse_mode="HTML", reply_markup=menu_kb(lang))
    ctx.user_data.clear()
    ctx.user_data["lang"] = lang
    return MENU

async def cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    lang = ctx.user_data.get("lang", "ru")
    await update.message.reply_text("❌ Отменено", reply_markup=menu_kb(lang))
    return MENU

def main():
    app = Application.builder().token(TOKEN).build()
    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            LANG:       [MessageHandler(filters.TEXT & ~filters.COMMAND, set_lang)],
            MENU:       [MessageHandler(filters.TEXT & ~filters.COMMAND, menu_handler)],
            FROM_WHERE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_from)],
            TO_WHERE:   [MessageHandler(filters.TEXT & ~filters.COMMAND, get_to)],
            CARGO_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_cargo)],
            TRANSPORT:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_transport)],
            WEIGHT:     [MessageHandler(filters.TEXT & ~filters.COMMAND, get_weight)],
            DIMENSIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_dimensions)],
            STACKABLE:  [MessageHandler(filters.TEXT & ~filters.COMMAND, get_stackable)],
            CONTACT:    [MessageHandler(filters.TEXT & ~filters.COMMAND, get_contact)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
        allow_reentry=True
    )
    app.add_handler(conv)
    print("✅ Бот запущен!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
