from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, FileField, SelectField, BooleanField, \
    PasswordField, FloatField
from wtforms.validators import DataRequired, ValidationError, EqualTo
from flask_wtf.file import FileAllowed
from application.core.models import Dish, DishCategory, User
import settings
from flask_login import current_user


#Форма создания категории
#Create category form
class CategoryForm(FlaskForm):
    name_ru = StringField('Название на русском', validators=[DataRequired('Укажите название категории на русском')])
    name_uz = StringField('Название на узбекском', validators=[DataRequired('Укажите название категории на узбексокм')])
    image = FileField('Изображение',
                      validators=[FileAllowed(['png', 'jpg', 'heic'],
                                              message='Разрешены только изображения форматов .jpg, .png')])
    parent = SelectField('Родительская категория', coerce=int)
    submit = SubmitField('Сохранить')

    def fill_from_object(self, category: DishCategory):
        self.name_ru.data = category.name
        self.name_uz.data = category.name_uz
        if category.parent:
            self.parent.data = category.parent_id


#Форма создания товара
#Create dish form
class DishForm(FlaskForm):
    name_ru = StringField('Название на русском', validators=[DataRequired('Укажите название блюда на русском')])
    name_uz = StringField('Название на узбекском', validators=[DataRequired('Укажите название блюда на узбексокм')])
    description_ru = TextAreaField('Описание товара на русском')
    description_uz = TextAreaField('Описание товара на узбекском')
    category = SelectField('Категория', validators=[DataRequired('Укажите категорию')], coerce=int)
    price = StringField('Цена', validators=[DataRequired('Укажите цену')])
    image = FileField('Изображение',
                      validators=[FileAllowed(['png', 'jpg', 'heic'],
                                              message='Разрешены только изображения форматов .jpg, .png')])
    delete_image = BooleanField('Удалить изображение')
    # show_usd = BooleanField('Показывать цену в долларах')
    submit = SubmitField('Сохранить')

    def fill_from_object(self, dish: Dish):
        self.name_ru.data = dish.name
        self.name_uz.data = dish.name_uz
        self.description_uz.data = dish.description_uz
        self.description_ru.data = dish.description
        self.category.data = dish.category_id
        self.price.data = dish.price
        # self.show_usd.data = dish.show_usd

    def validate_price(self, field):
        try:
            float(field.data)
        except ValueError:
            raise ValidationError('Укажите числовое значение цены')
        if float(field.data) <= 0:
            raise ValidationError('Цена не может быть отрицательной или равной нулю')


#Форма смены пароля администратора
#Administrator password change form
class AdministratorEmailForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired('Укажите e-mail')])
    password = PasswordField('Пароль', validators=[DataRequired('Для смены e-mail необходима аутентификация')])
    submit = SubmitField('Изменить')

    def fill_from_current_user(self):
        self.email.data = current_user.email

    def validate_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Указан неверный пароль')


#Форма смены пароля администратора
#Administrator password change form
class AdministratorPasswordForm(FlaskForm):
    current_password = PasswordField('Текущий пароль',
                                     validators=[DataRequired('Для смены пароля укажите текущий пароль')])
    new_password = PasswordField('Новый пароль', validators=[DataRequired("Введите новый пароль")])
    password_confirmation = PasswordField('Подтвердите новый пароль',
                                          validators=[EqualTo('new_password', 'Пароли должны совпадать')])
    submit = SubmitField('Изменить')

    def validate_password(self, field):
        if not current_user.check_password(field.data):
            raise ValidationError('Указан неверный пароль')


#Форма настройки цен на доставку
#Form for setting up delivery prices
class DeliveryPriceForm(FlaskForm):
    first_3_km = StringField('Стоимость за первые три киллометра',
                             validators=[DataRequired('Укажите стоимость первых трёх километров')])
    others_km = StringField('Стоимость за остальной путь',
                            validators=[DataRequired('Укажите стоимость за остальные километры')])
    limit_price = StringField('Лимит стоимости доставки',
                              validators=[DataRequired('Укажите лимит цены на доставку')])
    currency_value = StringField('Стоимость доллара, сум',
                                 validators=[DataRequired('Укажите стоимость доллара в суммах')])
    submit = SubmitField('Сохранить')

    def validate_int_value(self, field):
        if not field.data.isdigit():
            raise ValidationError("Стоимость доставки должна быть указана в цифрах")
        value = int(field.data)
        if value <= 0:
            raise ValidationError('Стоимость доставки должна быть больше нуля')

    def fill_from_settings(self):
        delivery_cost = settings.get_delivery_cost()
        self.first_3_km.data = delivery_cost[0]
        self.others_km.data = delivery_cost[1]
        self.limit_price.data = settings.get_limit_delivery_price()
        self.currency_value.data = settings.get_currency_value()

    def validate_first_3_km(self, field):
        self.validate_int_value(field)

    def validate_others_km(self, field):
        self.validate_int_value(field)

    def validate_limit_price(self, field):
        self.validate_int_value(field)

    def validate_currency_value(self, field):
        self.validate_int_value(field)


#Форма установки локации магазина
#Form for setting the store's location
class CafeLocationForm(FlaskForm):
    latitude = FloatField('Широта', validators=[DataRequired("Укажите широту")])
    longitude = FloatField('Долгота', validators=[DataRequired('Укажите долготу')])
    submit = SubmitField('Сохранить')

    def fill_from_settings(self):
        coordinates = settings.get_cafe_coordinates()
        self.latitude.data = coordinates[0]
        self.longitude.data = coordinates[1]


#Форма установки рабочего времени
#Working time setting form
class TimeSet(FlaskForm):
    start = StringField('Время от', validators=[DataRequired("Укажите время начала работы")])
    end = StringField('Время до', validators=[DataRequired('Укажите время конца работы')])
    notification = StringField('Введите текст уведомления', validators=[DataRequired("Укажите текст уведомления")])
    submit = SubmitField('Задать')

    def fill_from_settings(self):
        times = settings.get_timelimits()
        notify = settings.get_timenotify()
        self.notification.data = notify
        self.start.data = times[0]
        self.end.data = times[1]

    def validate_int_value(self, field):
        value = field.data

    def validate_start(self, field):
        self.validate_int_value(field)

    def validate_end(self, field):
        self.validate_int_value(field)


#Форма создания нового пользователя
#Adding new user form
class UserForm(FlaskForm):
    name = StringField('Имя пользователя', validators=[DataRequired("Укажите имя пользователя")])
    phone_number = StringField('Номер телефона', validators=[DataRequired("Укажите номер телефона")])
    submit = SubmitField('Сохранить')

    def fill_from_object(self, user: User):
        self.name.data = user.full_user_name
        self.phone_number = user.phone_number


#Форма рассылки
#Mailing form
class MailForm(FlaskForm):
    mail = StringField('Текст рассылки', validators=[DataRequired("Введите текст рассылки")])
    image = FileField('Изображение',
                      validators=[FileAllowed(['png', 'jpg', 'heic'],
                                              message='Разрешены только изображения форматов .jpg, .png')])

    submit = SubmitField('Разослать')




