from models.user_models import userManager
from datetime import datetime

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
        username = data.get('username')
        password = data.get('password')
        newPassword = data.get('newPassword')
        
        return userManager.doiMatKhau(username, password, newPassword)

    @staticmethod
    def capNhatHoSo(data):
        username = data.get('username')
        hoTen = data.get('hoTen')
        gioiTinh = data.get('gioiTinh')
        email = data.get('email')
        sdt = data.get('sdt')
        diaChi = data.get('diaChi')
        
        return userManager.capNhatHoSo(username, hoTen, gioiTinh, email, sdt, diaChi)