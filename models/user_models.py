from app import db
from werkzeug.security import generate_password_hash, check_password_hash #hask password
from flask import session

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
            return True, "Đăng nhập thành công"
        else:
            return False, "Sai tài khoản/mật khẩu"

    @classmethod
    def dangXuat(cls):
        return True, "Đăng Xuất Thành Công"

    @classmethod
    def doiMatKhau(cls, username, password, newPassword):
        user = cls.query.filter_by(username=username).first()
        if not check_password_hash(user.password, password):
            return False, "Mật Khẩu Cũ Không Đúng"
        
        if check_password_hash(user.password, newPassword):
            return False, "Trùng Mật Khẩu Cũ"
        
        if newPassword == "":
            return False, "Mật Khẩu Không Được Để Trống"
        
        user.password = generate_password_hash(newPassword, method='pbkdf2:sha256')
        db.session.commit()
        return True, "Đổi Mật Khẩu Thành Công"


    @classmethod
    def capNhatHoSo(cls, username, hoTen, gioiTinh, email, sdt, diaChi):
        user = cls.query.filter_by(username=username).first()
        user.hoTen = hoTen
        user.gioiTinh = gioiTinh
        user.email = email
        user.sdt = sdt
        user.diaChi = diaChi
        db.session.commit()
        return True, "Cập nhật thành công"