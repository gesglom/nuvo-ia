import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from lider_nuvo import ejecutar_mision_nuvo

TOKEN = '8688333324:AAG_IKRYbVDQsG5shl0ZnfkZxyxLKW6dDgg'
USUARIO_AUTORIZADO = 6650426868 # Ajusta con tu ID real

async def handle_mission(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != USUARIO_AUTORIZADO:
        return
    
    mision = update.message.text
    await update.message.reply_text(f'🚀 Misión recibida: "{mision}"\nEl equipo Nuvo está trabajando...')
    
    try:
        # Aquí el Líder realmente pone a trabajar a los agentes en la misión
        resultado = ejecutar_mision_nuvo(mision)
        await update.message.reply_text(f'✅ **RESULTADO DE LA MISIÓN**\n\n{resultado}')
    except Exception as e:
        await update.message.reply_text(f'❌ Error en la ejecución: {e}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_mission))
    print('📡 Nuvo en modo Misión Operativa...')
    app.run_polling()
