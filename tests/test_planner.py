import io,unittest
from openpyxl import Workbook
from planner import parse_file,plan,distance
from app import create_app
SAMPLE=b'nombre,lat,lon\nA,40.3,-3.7\nB,40.4,-3.8\nC,40.5,-3.9\n'
class PlannerTest(unittest.TestCase):
    def test_balanced(self):
        points=parse_file(SAMPLE,'a.csv');result=plan(points,2)
        self.assertEqual(sorted(p['id'] for r in result for p in r['stops']),[0,1,2])
        self.assertEqual([len(r['stops']) for r in result],[2,1]);self.assertGreater(result[0]['km'],0)
    def test_zero(self):
        p={'lat':40,'lon':-3};self.assertEqual(distance(p,p),0)
    def test_bad_files(self):
        for data,name in [(b'lat,lon\nNaN,2','a.csv'),(b'lat,lon\n91,2','a.csv'),(b'lat,lon\n,2','a.csv'),(b'x,y\n1,2','a.csv'),(b'bad','a.xlsx'),(b'x','a.exe')]:
            with self.subTest(name=name,data=data),self.assertRaises(ValueError):parse_file(data,name)
    def test_count(self):
        points=parse_file(SAMPLE,'a.csv')
        for n in [0,4,9,True,1.5]:
            with self.assertRaises(ValueError):plan(points,n)
    def test_xlsx(self):
        w=Workbook();w.active.append(['nombre','lat','lon']);w.active.append(['A',40.3,-3.7]);b=io.BytesIO();w.save(b)
        self.assertEqual(parse_file(b.getvalue(),'a.xlsx')[0]['name'],'A')
    def test_api(self):
        client=create_app().test_client();self.assertEqual(client.get('/health').json['status'],'ok')
        response=client.post('/api/plan',data={'file':(io.BytesIO(SAMPLE),'a.csv'),'routes':'2'})
        self.assertEqual(response.status_code,200);self.assertEqual(len(response.json['routes']),2)
        self.assertEqual(client.post('/api/plan').status_code,400)
    def test_origin_and_traversal(self):
        client=create_app().test_client();self.assertEqual(client.post('/api/plan',headers={'Origin':'https://other.invalid'}).status_code,403)
        self.assertEqual(client.get('/../app.py').status_code,404)
if __name__=='__main__':unittest.main()
