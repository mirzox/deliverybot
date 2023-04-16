from werkzeug.utils import secure_filename
from config import Config
from application.admin import bp
from flask_login import login_required
from flask import render_template, redirect, url_for, flash, request
from .forms import MailForm
from application import telegram_bot
import telebot
from application.core.models import User
import os


@bp.route('/mailing', methods=['GET', 'POST'])
@login_required
def mailing():
    mail_form = MailForm()
    if request.method == 'POST':
        file = request.files['image']
        file_name = file.filename
        if file:
            filename = secure_filename(file_name)
            file.save(os.path.join(Config.MAILING_DIRECTORY, filename))
        text = mail_form.mail.data
        file_id = None
        filepath = (Config.MAILING_DIRECTORY + file_name)
        users = User.query.all()
        if mail_form.image.data:
            for user in users:
                user_id = user.id
                if file_id:
                    try:
                        file = open(filepath, 'rb')
                        telegram_bot.send_photo(chat_id=user_id,
                                                photo=file_id,
                                                caption=text)
                        file.close()
                    except telebot.apihelper.ApiException:
                        continue
                else:
                    user_id = user.id
                    try:
                        file = open(filepath, 'rb')
                        file_id = telegram_bot.send_photo(chat_id=user_id,
                                                          photo=file,
                                                          caption=text).photo[-1].file_id
                        file.close()
                    except telebot.apihelper.ApiException:
                        continue
            #Изменено
            os.remove((Config.MAILING_DIRECTORY + "/" + file_name))
        else:
            for user in users:
                user_id = user.id
                try:
                    telegram_bot.send_message(chat_id=user_id,
                                              text=text)
                except telebot.apihelper.ApiException:
                    continue

        flash('Рассылка запущена!', category='success')
        return redirect(url_for('admin.mailing'))

    return render_template('admin/mailing.html',
                           title='Настройки',
                           area='mailing',
                           mail_form=mail_form)
