import pytest
import sqlite3
import os
from registration.registration import create_db, add_user, authenticate_user, display_users

@pytest.fixture(scope="module")
def setup_database():
    """Testlerden önce veri tabanını oluşturmak ve testlerden sonra temizlemek için kullanılan test düzeneği."""
    create_db()
    yield
    try:
        os.remove('users.db')
    except PermissionError:
        pass

@pytest.fixture
def connection():
    """Test sırasında veri tabanı bağlantısı oluşturur ve testten sonra bağlantıyı kapatır."""
    conn = sqlite3.connect('users.db')
    yield conn
    conn.close()


def test_create_db(setup_database, connection):
    """Veri tabanı ve 'users' tablosunun oluşturulmasını test eder."""
    cursor = connection.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
    table_exists = cursor.fetchone()
    assert table_exists, "'users' tablosu veri tabanında bulunmalıdır."

def test_add_new_user(setup_database, connection):
    """Yeni bir kullanıcının eklenmesini test eder."""
    add_user('testuser', 'testuser@example.com', 'password123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='testuser';")
    user = cursor.fetchone()
    assert user, "Kullanıcı veri tabanına eklenmiş olmalıdır."

def test_same_username(setup_database, connection):
    ao = add_user('a', 'ao@gmail.com', 'asd123')
    ai = add_user('a', 'ai@gmail.com', 'oshinoko123')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='a';")
    user = cursor.fetchone()
    assert user, "Kullanıcı eklenmemiş olmalıdır."

def test_authenticate_success(setup_database, connection):
    add_user('Mira', 'mira1512@hotmail.com', 'cecilia1512')
    authenticate_user('Mira', 'cecilia1512')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='Mira';")
    user = cursor.fetchone()
    assert user, "Kullanıcı doğrulanmış olmalıdır."

def test_wrong_password(setup_database, connection):
    add_user('Mira', 'mira1512@hotmail.com', 'cecilia1512')
    authenticate_user('Mira', 'cecliia1512')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='Mira';")
    user = cursor.fetchone()
    assert user, "Kullanıcı doğrulanmamış olmalıdır."

def test_userlist_success(setup_database, connection):
    add_user('Mira', 'mira1512@hotmail.com', 'cecilia1512')
    add_user('Emre', 'emrei@gmail.com', 'mira1512emre')
    display_users()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users;")
    user = cursor.fetchone()
    assert user, "Kullanıcıların listesi listelenmiş olmalıdır."

def test_nonexistentuser_authentication(setup_database, connection):
    authenticate_user('Mira', 'cecilia1512')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username='Mira';")
    user = cursor.fetchone()
    assert user, "Kullanıcı bulunamamış olmalıdır."


# İşte yazabileceğiniz bazı testler:
"""
Var olan bir kullanıcı adıyla kullanıcı eklemeye çalışmayı test etme. +??
Başarılı kullanıcı doğrulamasını test etme. ++?
Var olmayan bir kullanıcıyla doğrulama yapmayı test etme.+++
Yanlış şifreyle doğrulama yapmayı test etme. +++
Kullanıcı listesinin doğru şekilde görüntülenmesini test etme. +++
"""
