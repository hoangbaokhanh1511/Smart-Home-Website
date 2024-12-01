from models.user_models import userManager
from datetime import datetime
from flask import session

class userController:

    @staticmethod
    def dangKy(data):
        username = data.get('username')
        password = data.get('password')
        hoTen = data.get('hoTen')
        email = data.get('email')
        sdt = data.get('sdt')
        diaChi = data.get('diaChi')
        gioiTinh = data.get('gioiTinh') == 'Nam' if data.get('gioiTinh') else None
        ngaySinh = datetime.strptime(data.get('ngaySinh'), '%Y-%m-%d').date() if data.get('ngaySinh') else None
        return userManager.dangKy(username, password, hoTen, email, sdt, diaChi , gioiTinh, ngaySinh)

    @staticmethod
    def dangNhap(data):
        
        username = data.get('username')
        password = data.get('password')
        
        return userManager.dangNhap(username, password)

    @staticmethod
    def dangXuat():
        return userManager.dangXuat()

    @staticmethod
    def doiMatKhau(data):

        oldPassword = data.get('oldPassword')
        newPassword = data.get('newPassword')
        repeatPassword = data.get('repeatPassword')
        username = session.get('username')
        return userManager.doiMatKhau(username, oldPassword, newPassword, repeatPassword)

    @staticmethod
    def capNhatHoSo(data):
        name = data.get('newName')
        email = data.get('newEmail')
        gioiTinh = data.get('newGender')
        ngaySinh = data.get('newBirthday')
        sdt = data.get('newPhone')
        diaChi = data.get('newAddress')
        
        return userManager.capNhatHoSo(name, email, gioiTinh, ngaySinh, sdt, diaChi)
    