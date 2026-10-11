from remnawave.models.hosts import GetAllHostsResponseDto, UpdateHostRequestDto
from remna import remna


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_TOKEN, TAG, ADMINS


bot = Bot(BOT_TOKEN)
dp = Dispatcher()


async def main(domain: str):
    hosts: GetAllHostsResponseDto = await remna.hosts.get_all_hosts()
    tag_hosts = []
    for host in hosts:
        if TAG in host.tags:
            tag_hosts.append(host)
    for host in tag_hosts:
        address = host.address.split(".")[0] + "." + domain
        await remna.hosts.update_host(
            UpdateHostRequestDto(
                uuid=host.uuid,
                address=address
            )
        )


@dp.message(Command("start"))
async def start(message: Message):
    if message.from_user.id in ADMINS:
        await message.answer("Отправьте домен, на который хотите изменить")


@dp.message(F.text)
async def change_domain(message: Message):
    if message.from_user.id in ADMINS:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [
                InlineKeyboardButton(text="Да ✅", callback_data="confirm_change_"+message.text),
                InlineKeyboardButton(text="Нет ❌", callback_data="cancel")
            ]
        ])
        await message.answer(f"Вы уверены, что хотите изменить домен на {message.text} ?", reply_markup=kb)


@dp.callback_query(F.data.startswith("confirm_change_"))
async def confirm_change(call: CallbackQuery):
    if call.from_user.id in ADMINS:
        await call.message.edit_text("Редактирую...", reply_markup=InlineKeyboardMarkup(inline_keyboard=[]))
        domain = call.data.removeprefix("confirm_change_")
        await main(domain)
        await call.message.edit_text(f"✅ Домен изменён на {domain}")


@dp.callback_query(F.data == "cancel")
async def cancel_change(call: CallbackQuery):
    await call.message.edit_text("❌ Редактирование отменено")


import asyncio
asyncio.run(dp.start_polling(bot))
