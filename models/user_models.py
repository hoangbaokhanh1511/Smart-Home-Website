from app import db
from werkzeug.security import generate_password_hash, check_password_hash #hash password
from flask import session
from datetime import datetime

class userManager(db.Model):
    __tablename__ = 'user_manager'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    hoTen = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    gioiTinh = db.Column(db.Boolean)
    ngaySinh = db.Column(db.Date)
    sdt = db.Column(db.String(15))
    diaChi = db.Column(db.String(255))

    @classmethod
    def dangKy(cls, username, password, hoTen, email, sdt, address, gioiTinh=None, ngaySinh=None):
        if cls.query.filter_by(username=username).first():
            return False, "Tài Khoản đã tồn tại"

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = cls(username=username, password=hashed_password, hoTen=hoTen, 
                        email=email, sdt=sdt, gioiTinh=gioiTinh, ngaySinh=ngaySinh, diaChi=address)
        db.session.add(new_user)
        db.session.commit()
        return True, "Đăng ký thành công"

    @classmethod
    def dangNhap(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password,password):
            session['username'] = user.username
            session['id'] = generate_password_hash(str(user.id))
            return True, "Đăng nhập thành công"
        else:
            return False, "Sai tài khoản/mật khẩu"

    @classmethod
    def dangXuat(cls):
        return True, "Đăng Xuất Thành Công"

    @classmethod
    def doiMatKhau(cls, username, oldPassword, newPassword, repeatPassword):
        user = cls.query.filter_by(username=username).first()
        
        if not check_password_hash(user.password, oldPassword):
            return False, "Mật Khẩu Cũ Không Đúng"
        
        if check_password_hash(user.password, newPassword):
            return False, "Trùng Mật Khẩu Cũ"
        
        if newPassword != repeatPassword:
            return False, "Nhập Không Trùng Với Mật Khẩu Mới"
        
        user.password = generate_password_hash(newPassword, method='pbkdf2:sha256')
        db.session.commit()
        return True, "Đổi Mật Khẩu Thành Công"


    @classmethod
    def capNhatHoSo(cls, name, email, gioiTinh, ngaySinh, sdt, diaChi):
        user = cls.query.filter_by(username=session['username']).first()
        if name:
            user.hoTen = name
        if email:
            user.email = email
        if gioiTinh:
            user.gioiTinh = bool(gioiTinh)
        if ngaySinh:
            user.ngaySinh = datetime.strptime(ngaySinh, '%Y-%m-%d').date()
        if sdt:
            user.sdt = sdt
        if diaChi:
            user.diaChi = diaChi
        db.session.commit()
        return True, "Cập nhật thành công"
    
    @classmethod
    def findUser(cls, username):
        user = cls.query.filter_by(username=username).first()
        name = user.hoTen
        email = user.email
        gender = user.gioiTinh
        birthday = user.ngaySinh
        phone = user.sdt
        address = user.diaChi
        return name, email, gender, birthday, phone, address