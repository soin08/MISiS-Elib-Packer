import os
import shutil
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import mechanicalsoup


class Packer_BaseError(Exception):
    pass

class Packer_LoginError(Packer_BaseError):
    pass


class Packer:
    def __init__(self):
        self.browser = mechanicalsoup.Browser()

    def login(self, username, password):
        login_page = self.browser.get('http://elibrary.misis.ru/login.php')

        login_form = login_page.soup.select('#formbox')[0].select('form')[0]

        # specify username and password
        login_form.find(id="username")['value'] = username
        login_form.find(id="password")['value'] = password

        page2 = self.browser.submit(login_form, login_page.url)

        # verify we are now logged in
        if page2.soup.find(class_='ktErrorMessage'):
            raise Packer_LoginError('Неправильный логин / пароль')

    def save_book(self, book_id):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        tmp_dir = base_dir + '/tmp'
        pdf_path = base_dir + '/book_' + str(book_id) + '.pdf'
        c = canvas.Canvas(pdf_path)

        page = 0

        if not os.path.exists(tmp_dir):
            os.makedirs(tmp_dir)

        while True:
            img_path = base_dir + '/tmp/image_' + str(page) + '.jpg'

            response = self.browser.get('http://elibrary.misis.ru/plugins/SecView/getDoc.php?id='+ str(book_id) +'&page='+ str(page) +'&type=large/fast',
                                         stream=True)

            #quit if it isn't an image
            if not response.headers['content-type'] == 'image/jpeg':
                break

            #save image
            with open(img_path, 'wb') as out_file:
                 shutil.copyfileobj(response.raw, out_file)

            del response

            #add image to pdf
            im = ImageReader(img_path)
            imagesize  = im.getSize()
            c.setPageSize(imagesize)
            c.drawImage(img_path,0,0)
            c.showPage()
            c.save()

            #remove image
            os.remove(img_path)

            page += 1

        #remove tmp folder
        os.rmdir(tmp_dir)

    def logout(self):
        self.browser.get('http://elibrary.misis.ru/presentation/logout.php')
