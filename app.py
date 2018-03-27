# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import errno
import os
import sys
import tempfile
from argparse import ArgumentParser

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from listBerita import listBerita
from rangkum import Berita
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageTemplateAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URITemplateAction,
    PostbackTemplateAction, DatetimePickerTemplateAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent
)

app = Flask(__name__)

line_bot_api = LineBotApi('XSnZePrtWTJ/4ljO7vOGY5gYzpu9O81cL1osgf4tdhtKhhMgRkErlcjmGLikCo/44gwzAhjzMmx2QcgDsDz9sISMUX1h3AMYIUq4EXf+8qWaOgJwxLaWIDglpFpT08O8qH6QIjRodb4oVi0714yomAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('89359153657f76c1a67fcbb4fd773436')

static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

def make_static_tmp_dir():
    try:
        os.makedirs(static_tmp_path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(static_tmp_path):
            pass
        else:
            raise

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

def eyny_movie():
    target_url = 'http://www.eyny.com/forum-205-1.html'
    print('Start parsing eynyMovie....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ''
    for titleURL in soup.select('.bm_c tbody .xst'):
        if pattern_mega(titleURL.text):
            title = titleURL.text
            if '11379780-1-3' in titleURL['href']:
                continue
            link = 'http://www.eyny.com/' + titleURL['href']
            data = '{}\n{}\n\n'.format(title, link)
            content += data
    return content

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    text = event.message.text
    if "/stalk " in text.lower():
        user = text.lower().replace("/stalk ","")
        r = request.get('http://api.secold.com/instagram/stalk/'+user+'/postlimit/6')
        data = r.text
        data = json.loads(data)
        private = data['results']
        if private == []:
            line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(
                    text="Failed, User mungkin di private atau post kurang dari 6"
                    )
                ]
                )
        else:
            image_carousel_template = ImageCarouselTemplate(columns=[
                ImageCarouselColumn(image_url=data['results'][0]['url'],
                                    actions=URITemplateAction(
                                        label='Save', url=data['results'][0]['url'])),
                ImageCarouselColumn(image_url=data['results'][1]['url'],
                                    actions=URITemplateAction(
                                        label='Save', url=data['results'][1]['url'])),
                ImageCarouselColumn(image_url=data['results'][2]['url'],
                                    actions=URITemplateAction(
                                        label='Save', url=data['results'][2]['url']))
            ])
            line_bot_api.reply_message(
                event.reply_token, [
                TemplateSendMessage(
                    alt_text='Stalk Instagram',
                    template=image_carousel_template
                    )
                ]
                )



    elif text == '/bye':
        if isinstance(event.source, SourceGroup):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Owner : http://line.me/ti/p/~bali999'))
            line_bot_api.leave_group(event.source.group_id)
        elif isinstance(event.source, SourceRoom):
            line_bot_api.reply_message(
                event.reply_token, TextMessage(text='Owner : http://line.me/ti/p/~bali999'))
            line_bot_api.leave_room(event.source.room_id)
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextMessage(text="Bot can't leave from 1:1 chat"))
    elif text == 'confirm':
        confirm_template = ConfirmTemplate(text='Do it?', actions=[
            MessageTemplateAction(label='Yes', text='Yes!'),
            MessageTemplateAction(label='No', text='No!'),
        ])
        template_message = TemplateSendMessage(
            alt_text='Confirm alt text', template=confirm_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == '/buttons':
        buttons_template = ButtonsTemplate(
            title='List Pr', text='Klik salah satu', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping'),
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ])
        template_message = TemplateSendMessage(
            alt_text='Buttons alt text', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)
        
    elif text == 'carousel':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text='hoge1', title='fuga1', actions=[
                URITemplateAction(
                    label='Go to line.me', uri='https://line.me'),
                PostbackTemplateAction(label='ping', data='ping')
            ]),
            CarouselColumn(text='hoge2', title='fuga2', actions=[
                PostbackTemplateAction(
                    label='ping with text', data='ping',
                    text='ping'),
                MessageTemplateAction(label='Translate Rice', text='米')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'Pr':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR',
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
                PostbackTemplateAction(label='Pkn', data='pkn'),
                PostbackTemplateAction(label='Kimia', data='kimia'),
            ]),
            CarouselColumn(
            	text='Klik salah satu',
            	title='List PR',
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Bhs.Bali', data='bali'),
            	PostbackTemplateAction(label='Agama', data='agama'),
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Kwu', data='kwu'),
            	PostbackTemplateAction(label='Ips', data='ips'),
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Fisika', data='fisika'),
            	PostbackTemplateAction(label='Matematika', data='matik'),
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Kkpi', data='kkpi'),
            	MessageTemplateAction(label='Ipa', text='Pr ipa')
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='English', data='inggris'),
            	PostbackTemplateAction(label='Seni Budaya', data='senbud')
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Budi pekerti', data='budi'),
            	PostbackTemplateAction(label='Bhs.Indonesia', data='indo')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'Jadwal':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
            	text='Klik salah satu', 
            	title='Jadwal',
            	thumbnail_image_url='https://i.imgur.com/2dZuLj8.jpg',
            	actions=[
                PostbackTemplateAction(label='Senin', data='senin'),
                PostbackTemplateAction(label='Selasa', data='selasa'),
                PostbackTemplateAction(label='Rabu', data='rabu')
            ]),
            CarouselColumn(
            	text='Klik salah satu',
            	title='Jadwal',
            	thumbnail_image_url='https://i.imgur.com/8yVTyeg.jpg',
            	actions=[
            	PostbackTemplateAction(label='Kamis', data='kamis'),
            	PostbackTemplateAction(label='Jumat', data='jumat'),
            	PostbackTemplateAction(label='Sabtu', data='sabtu')
            ]),
        ])
        template_message = TemplateSendMessage(
            alt_text='Carousel alt text', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'Bantuan':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
            	text='Klik salah satu', 
            	title='Jadwal',
            	thumbnail_image_url='https://i.imgur.com/mMi5Umy.jpg',
            	actions=[
                PostbackTemplateAction(label='Jadwal', data='jadwal')
            ]),
            CarouselColumn(
            	text='Klik salah satu',
            	title='List PR',
            	thumbnail_image_url='https://i.imgur.com/RXHhM4U.jpg',
            	actions=[
            	PostbackTemplateAction(label='List PR', data='pr')
           	]),
           	CarouselColumn(
            	text='Klik salah satu',
            	title='Jadwal UAS',
            	thumbnail_image_url='https://i.imgur.com/BxbJ52i.jpg',
            	actions=[
            	MessageTemplateAction(label='Jadwal UAS', text='/jadwal uas')
            ])
        ])
        template_message = TemplateSendMessage(
            alt_text='Bantuan', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'tekno':
        databerita = listBerita("http://tekno.kompas.com/business")
        daftarberita = databerita.daftarBerita()    
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text=daftarberita[acak[0]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[0]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[0]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[1]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[1]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[1]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[2]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[2]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[2]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[3]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[3]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[3]]['link'])
            ])
        ])
        template_message = TemplateSendMessage(
            alt_text='Daftar Berita Tekno', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'bisnis':
        databerita = listBerita("http://bisniskeuangan.kompas.com/bisnis")
        daftarberita = databerita.daftarBerita()
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text=daftarberita[acak[0]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[0]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[0]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[1]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[1]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[1]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[2]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[2]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[2]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[3]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[3]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[3]]['link'])
            ])
        ])
        template_message = TemplateSendMessage(
            alt_text='Daftar Berita Bisnis', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)
    elif text == 'otomotif':
        databerita = listBerita("http://otomotif.kompas.com/news")
        daftarberita = databerita.daftarBerita()
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(text=daftarberita[acak[0]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[0]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[0]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[1]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[1]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[1]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[2]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[2]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[2]]['link'])
            ]),
            CarouselColumn(text=daftarberita[acak[3]]['judul'],  actions=[
                PostbackTemplateAction(label="Ringkas", data=daftarberita[acak[3]]['link'], text='ringkas'),
                URITemplateAction(label='Baca berita asli', uri=daftarberita[acak[3]]['link'])
            ])
        ])
        template_message = TemplateSendMessage(
            alt_text='Daftar Berita Otomotif', template=carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'About':
        buttons_template = ButtonsTemplate(
                    text='Main Developer',
                    title='Bali Tenaya',
                    thumbnail_image_url='https://i.imgur.com/cltOVPI.jpg',
                    actions=[
                    URITemplateAction(label='instagram', uri='https://www.instagram.com/tenaya_bali/'),
                   	URITemplateAction(label='Twitter', uri='https://www.twitter.com/tenaya_bali/')
                ])
        template_message = TemplateSendMessage(
            alt_text='About', template=buttons_template)
        line_bot_api.reply_message(event.reply_token, template_message)

    elif text == 'image_carousel':
        image_carousel_template = ImageCarouselTemplate(columns=[
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='datetime',
                                                                    data='datetime_postback',
                                                                    mode='datetime')),
            ImageCarouselColumn(image_url='https://via.placeholder.com/1024x1024',
                                action=DatetimePickerTemplateAction(label='date',
                                                                    data='date_postback',
                                                                    mode='date'))
        ])
        template_message = TemplateSendMessage(
            alt_text='ImageCarousel alt text', template=image_carousel_template)
        line_bot_api.reply_message(event.reply_token, template_message)

@handler.add(MessageEvent, message=LocationMessage)
def handle_location_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        LocationSendMessage(
            title=event.message.title, address=event.message.address,
            latitude=event.message.latitude, longitude=event.message.longitude
        )
    )

# Other Message Type
@handler.add(MessageEvent, message=(ImageMessage, VideoMessage, AudioMessage))
def handle_content_message(event):
    if isinstance(event.message, ImageMessage):
        ext = 'jpg'
    elif isinstance(event.message, VideoMessage):
        ext = 'mp4'
    elif isinstance(event.message, AudioMessage):
        ext = 'm4a'
    else:
        return

    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix=ext + '-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '.' + ext
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save content.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(MessageEvent, message=FileMessage)
def handle_file_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with tempfile.NamedTemporaryFile(dir=static_tmp_path, prefix='file-', delete=False) as tf:
        for chunk in message_content.iter_content():
            tf.write(chunk)
        tempfile_path = tf.name

    dist_path = tempfile_path + '-' + event.message.file_name
    dist_name = os.path.basename(dist_path)
    os.rename(tempfile_path, dist_path)

    line_bot_api.reply_message(
        event.reply_token, [
            TextSendMessage(text='Save file.'),
            TextSendMessage(text=request.host_url + os.path.join('static', 'tmp', dist_name))
        ])


@handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token, TextSendMessage(text='PAYPAL : http://bit.ly/2F9qKHU\n\nDONATE : http://bit.ly/2Fj3ZUU'))


@handler.add(UnfollowEvent)
def handle_unfollow():
    app.logger.info("Got Unfollow event")


@handler.add(JoinEvent)
def handle_join(event):
    buttons_template = ButtonsTemplate(
            	text='Harap Menggunakan Bot dengan bijak', 
            	title='GOVERIT',
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
                PostbackTemplateAction(label='Bantuan', data='/bantuan')
    ])
    line_bot_api.reply_message(
                event.reply_token, [
                TextSendMessage(
                    text="Hai Kak, Ada yang bisa gue bantu? Tap Bantuan aja yak :)"
                    ),
                TemplateSendMessage(
                    alt_text='Bantuan', 
                    template=buttons_template
                    )
                ]
                )

@handler.add(LeaveEvent)
def handle_leave():
    app.logger.info("Got leave event")


@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == 'ping':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='pong'))
    elif event.postback.data == 'datetime_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['datetime']))
    elif event.postback.data == 'date_postback':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.postback.params['date']))
   
@handler.add(PostbackEvent)
def handle_postback(event):
    if event.postback.data == '/bantuan':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
            	text='Klik salah satu', 
            	title='Jadwal',
            	thumbnail_image_url='https://i.imgur.com/mMi5Umy.jpg',
            	actions=[
                PostbackTemplateAction(label='Jadwal', data='jadwal')
            ]),
            CarouselColumn(
            	text='Klik salah satu',
            	title='List PR',
            	thumbnail_image_url='https://i.imgur.com/RXHhM4U.jpg',
            	actions=[
            	PostbackTemplateAction(label='List PR', data='pr')
           	]),
           	CarouselColumn(
            	text='Klik salah satu',
            	title='Jadwal UAS',
            	thumbnail_image_url='https://i.imgur.com/BxbJ52i.jpg',
            	actions=[
            	MessageTemplateAction(label='Jadwal UAS', text='/jadwal uas')
            ])
        ])
        line_bot_api.reply_message(
            event.reply_token, [
            TemplateSendMessage(
                alt_text='bantuan', 
                template=carousel_template
                )
            ]
            )
    elif event.postback.data == 'pr':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR',
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
                PostbackTemplateAction(label='Pkn', data='pkn'),
                PostbackTemplateAction(label='Kimia', data='kimia'),
            ]),
            CarouselColumn(
            	text='Klik salah satu',
            	title='List PR',
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Bhs.Bali', data='bali'),
            	PostbackTemplateAction(label='Agama', data='agama'),
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Kwu', data='kwu'),
            	PostbackTemplateAction(label='Ips', data='ips'),
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Fisika', data='fisika'),
            	PostbackTemplateAction(label='Matematika', data='matik'),
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Kkpi', data='kkpi'),
            	MessageTemplateAction(label='Ipa', text='Pr ipa')
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='English', data='inggris'),
            	PostbackTemplateAction(label='Seni Budaya', data='senbud')
            ]),
            CarouselColumn(
            	text='Klik salah satu', 
            	title='List PR', 
            	thumbnail_image_url='https://i.imgur.com/zWJqolN.jpg',
            	actions=[
            	PostbackTemplateAction(label='Budi pekerti', data='budi'),
            	PostbackTemplateAction(label='Bhs.Indonesia', data='indo')
            ]),
        ])
        line_bot_api.reply_message(
            event.reply_token, [
            TemplateSendMessage(
                alt_text='List pr', 
                template=carousel_template
                )
            ]
            )
    elif event.postback.data == 'jadwal':
        carousel_template = CarouselTemplate(columns=[
            CarouselColumn(
            	text='Klik salah satu', 
            	title='Jadwal',
            	thumbnail_image_url='https://i.imgur.com/2dZuLj8.jpg',
            	actions=[
                PostbackTemplateAction(label='Senin', data='senin'),
                PostbackTemplateAction(label='Selasa', data='selasa'),
                PostbackTemplateAction(label='Rabu', data='rabu')
            ]),
            CarouselColumn(
            	text='Klik salah satu',
            	title='Jadwal',
            	thumbnail_image_url='https://i.imgur.com/8yVTyeg.jpg',
            	actions=[
            	PostbackTemplateAction(label='Kamis', data='kamis'),
            	PostbackTemplateAction(label='Jumat', data='jumat'),
            	PostbackTemplateAction(label='Sabtu', data='sabtu')
            ])
        ])
        line_bot_api.reply_message(
            event.reply_token, [
            TemplateSendMessage(
                alt_text='Jadwal', 
                template=carousel_template
                )
            ]
            )
    elif event.postback.data == 'senbud':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Seni Budaya ]\n\nPraktek tarian + makalah'))
    elif event.postback.data == 'pkn':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Pkn ]\n\n-'))
    elif event.postback.data == 'kimia':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Kimia ]\n\n-'))
    elif event.postback.data == 'inggris':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Bhs.Inggris ]\n\n-'))
    elif event.postback.data == 'bali':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Bhs.Bali ]\n\n-'))
    elif event.postback.data == 'agama':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Agama ]\n\n-'))
    elif event.postback.data == 'kwu':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Kwu ]\n\nMembuat Proposal Tentang sebuah perusahaan. Dikumpul sebelum USBN'))
    elif event.postback.data == 'ips':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Ips ]\n\n-'))
    elif event.postback.data == 'budi':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Budi Pekerti ]\n\nMembuat kliping tentang bencana alam'))
    elif event.postback.data == 'fisika':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Fisika ]\n\n-'))
    elif event.postback.data == 'matik':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Matematika ]\n\n-'))
    elif event.postback.data == 'indo':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Bhs.Indonesia ]\n\nMembuat Surat Lamaran kerja + Iklan lamaran kerja , Map biru + Double folio Dikumpul Paling lambat Hari kamis (15/03/2018)'))
    elif event.postback.data == 'kkpi':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Tugas Kkpi ]\n\n-'))
    elif event.postback.data == 'senin':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Senin ]\n\n- Bhs.inggris\n- Kimia\n- Pkn'))
    elif event.postback.data == 'selasa':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Selasa ]\n\n- Bhs.inggris\n- Bhs.bali\n- Agama\n- Seni budaya'))
    elif event.postback.data == 'rabu':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Rabu ]\n\n- Kejuruan\n- olahraga'))
    elif event.postback.data == 'kamis':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Kamis ]\n\n- Kwu\n- Ips\n- Agama\n- Budi pekerti\n- Bhs.indonesia'))
    elif event.postback.data == 'jumat':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Jumat ]\n\n- P.wali\n- Fisika\n- Kejuruan'))
    elif event.postback.data == 'sabtu':
        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text='[ Sabtu ]\n\n- Matematika\n- Kkpi\n- Ipa'))

@handler.add(BeaconEvent)
def handle_beacon(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(
            text='Got beacon event. hwid={}, device_message(hex string)={}'.format(
                event.beacon.hwid, event.beacon.dm)))


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
