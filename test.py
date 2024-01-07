from flask import Flask
from unittest import TestCase
from app import app, User,db, connect_db,Post

class UnitTestCase(TestCase):
    def setUp(self):
        """Stuff to do before every test."""
        # connect_db(app)
        db.drop_all()
        db.create_all()

        user_one = User(first_name="Bob",last_name="Trika",image_url="https://images.pexels.com/photos/9304725/pexels-photo-9304725.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500")
        user_two = User(first_name="Jess",last_name="Trika",image_url="https://media.istockphoto.com/id/183821822/photo/say.webp?b=1&s=170667a&w=0&k=20&c=swQJgX34XSWBCtqou5XITqpOAxukOWX5Lh3PiZh3R18=")
        user_three = User(first_name="Dylan",last_name="Trika",image_url="https://media.istockphoto.com/id/172947045/photo/black-white-and-gray-tiles-full-frame-background.webp?b=1&s=170667a&w=0&k=20&c=cZ60Vs7I9i6yJDDcub9nh-F6caKS-6pVWc8UW2-vRXA=")

        db.session.add(user_one)
        db.session.add(user_two)
        db.session.add(user_three)

        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_welcome(self):
        with app.test_client() as client:
            resp = client.get('/',follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertIn('<h1>Users</h1>', html)
        self.assertEqual(resp.status_code, 200)
    
    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get('/users')
        html = resp.get_data(as_text=True)

        self.assertIn('<h1>Users</h1>', html)
        self.assertIn('Bob Trika', html)
        self.assertIn('Jess Trika', html)
        self.assertIn('Dylan Trika', html)
        self.assertEqual(resp.status_code, 200)

    def test_user_form(self):
        with app.test_client() as client:
            resp = client.get('/users/new')
        html = resp.get_data(as_text=True)

        self.assertIn('Create a User', html)
        self.assertEqual(resp.status_code, 200)
    
    def test_details(self):
        client = app.test_client()
        resp1 = client.get('/users/1')
        html = resp1.get_data(as_text=True)

        self.assertIn('Bob Trika',html)
        resp2 = client.get('/users/2')
        html = resp2.get_data(as_text=True)

        self.assertIn('Jess Trika',html)
        resp3 = client.get('/users/3')
        html = resp3.get_data(as_text=True)

        self.assertIn('Dylan Trika',html)
        self.assertEqual(resp1.status_code, 200)
    
    def test_creating_user(self):
        client = app.test_client()
        resp1 = client.post('/users/new', follow_redirects=True, data ={'first_name':'Dublin','last_name':'Trika','image_url':'https://img.buzzfeed.com/buzzfeed-static/static/2018-03/30/13/campaign_images/buzzfeed-prod-web-02/29-cool-and-random-things-you-can-probably-afford-2-3151-1522429262-9_dblbig.jpg?resize=1200:*'})
        html = resp1.get_data(as_text=True)

        self.assertIn('Dublin Trika',html)
        self.assertEqual(resp1.status_code, 200)
    
    def test_delete(self):
        client = app.test_client()
        resp1 = client.get('users/1/delete',follow_redirects=True)
        resp2 = client.get('users/2/delete')
        resp3 = client.get('/users')
        html = resp3.get_data(as_text=True)

        self.assertIn('Dylan Trika', html)
        self.assertEqual(resp1.status_code, 200)
    
    def test_show_post_form(self):
        client = app.test_client()
        resp1 = client.get('users/1/posts/new')
        html1 = resp1.get_data(as_text=True)

        client = app.test_client()
        resp2 = client.get('users/2/posts/new')
        html2 = resp2.get_data(as_text=True)

        self.assertIn('Add Post',html1)
        self.assertIn('Add Post',html2)
        self.assertEqual(resp1.status_code, 200)
        
    def test_make_form(self):
        client = app.test_client()
        resp1 = client.post('users/1/posts/new',follow_redirects=True,data={'title':'nice recipe','content':'pancakes without eggs'})
        html1 = resp1.get_data(as_text=True)

        self.assertIn('nice recipe',html1)
        self.assertEqual(resp1.status_code, 200)

    def test_show_post(self):
        post_one = Post(title="nice recipe",content="pancake without eggs", created_at="01-05-2013 9:23 PM", user_id =1)
        post_two =Post(title="better recipe",content="pancake with eggs", created_at="01-05-2013 9:24 PM", user_id =2)
        db.session.add(post_one)
        db.session.add(post_two)
        db.session.commit()

        client = app.test_client()
        resp1 = client.get('/posts/1')
        html1 = resp1.get_data(as_text=True)

        resp2 = client.get('/posts/2')
        html2 = resp2.get_data(as_text=True)

        self.assertIn('nice recipe', html1)
        self.assertIn('better recipe', html2)
        self.assertEqual(resp1.status_code, 200)
    
    def test_delete_post(self):
        post_one = Post(title="nice recipe",content="pancake without eggs", created_at="01-05-2013 9:23 PM", user_id =1)
        post_two =Post(title="better recipe",content="pancake with eggs", created_at="01-05-2013 9:24 PM", user_id =2)
        db.session.add(post_one)
        db.session.add(post_two)
        db.session.commit()

        client = app.test_client()
        resp1 = client.post('/posts/1/delete')
        resp2 = client.get('/posts/2')
        html1 = resp2.get_data(as_text=True)

        self.assertIn('better recipe', html1)




