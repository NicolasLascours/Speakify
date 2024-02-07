import os
import unittest
from app import app
from utils import allowed_file, clean_downloads_folder

class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def tearDown(self):
        pass

    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_file_upload(self):
        data = {
            'file': (open('test_file.txt', 'rb'), 'test_file.txt')
        }
        response = self.app.post('/', data=data, content_type='multipart/form-data', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
    
class TestUtils(unittest.TestCase):

    def test_allowed_file(self):
        self.assertTrue(allowed_file('file.txt'))
        self.assertTrue(allowed_file('document.pdf'))
        self.assertTrue(allowed_file('report.docx'))

        self.assertFalse(allowed_file('image.jpg'))
        self.assertFalse(allowed_file('data.csv'))
        self.assertFalse(allowed_file('script.py'))

        # Test files without extensions
        self.assertFalse(allowed_file('file'))
        self.assertFalse(allowed_file('document'))
        self.assertFalse(allowed_file('report'))

    def test_clean_downloads_folder(self):
        folder_path = 'temp_folder'
        os.makedirs(folder_path, exist_ok=True)
        open(os.path.join(folder_path, 'file1.txt'), 'w').close()
        open(os.path.join(folder_path, 'file2.pdf'), 'w').close()

        # Ensure files were created
        self.assertTrue(os.path.exists(os.path.join(folder_path, 'file1.txt')))
        self.assertTrue(os.path.exists(os.path.join(folder_path, 'file2.pdf')))

        clean_downloads_folder(folder_path)

        # Ensure files were deleted
        self.assertFalse(os.path.exists(os.path.join(folder_path, 'file1.txt')))
        self.assertFalse(os.path.exists(os.path.join(folder_path, 'file2.pdf')))

        # Remove the temporary folder
        os.rmdir(folder_path)

if __name__ == '__main__':
    unittest.main()
