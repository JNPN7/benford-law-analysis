from pyramid.view import view_config
from ..utils import *
import json

@view_config(route_name='benford', renderer='benford_law_pyramid:templates/benford.jinja2')
def benford(request):

    if request.method == "POST":
        try:
            csv_file = request.POST['csvFile'].file
            file_name = request.POST['csvFile'].filename
        except:
            return {"error": "Please upload a file"}

        name, ext = file_name.split('.')

        if ext != 'csv':
            return {"error": "Please upload csv file"}
        else:
            filepath = "uploads/data.csv"
            with open(filepath,"wb") as f:
                f.write(csv_file.read())
            
            data_distribution = get_data_distribution(filepath)

            if check_benford_law(filepath):
                filepath = f"uploads/{name}.json"
                with open(filepath,"w") as f:
                    json.dump(data_distribution, f)

                message = "The data follows Benford's law"
            else:
                message = "The data doesn't follow Benford's law"
                
            result =  {
                "message": message,
                "distribution": data_distribution
            }
            return result

    return {}
