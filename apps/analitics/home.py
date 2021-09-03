import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, Output
import dash
import os
from app import app
import flask

url_back=app.get_asset_url('img/bg_image_1.png')
url_back2=app.get_asset_url('img/bg_lateral.png')
url_css1=app.get_asset_url('css/bootstrap.css')
url_css2=app.get_asset_url('css/theme.css')

layout = html.Div([
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Bucaramanga</title>
  <link rel="stylesheet" href="'''+url_css1+'''">
  <link rel="stylesheet" href="'''+url_css2+'''">
</head>
<body>
  <div class="back-to-top"></div>

  <header>
    

  <div class="page-hero bg-image overlay-dark" style="background-image: url(https://turequerimientoya.com/wp-content/uploads/2021/01/tr%C3%A1nsito-bucaramanga-1.jpg);">
    <div class="hero-section">
      <div class="container text-center wow zoomIn">
        <span class="subhead">Vulnerability</span>
        <h1 class="display-4">Child and young people</h1>
      </div>
    </div>
  </div>


  <div class="bg-light">
    <div class="page-section py-3 mt-md-n5 custom-index">
      <div class="container">
        <div class="row justify-content-center">
          <div class="col-md-4 py-3 py-md-0">
            <div class="card-service wow fadeInUp">
              <div class="circle-shape bg-secondary text-white">
                <span>SV</span>
              </div>
              <p><span>SURVIVAL</span>
              <UL style="background-color: white;font-size: 15px;">
                <li>Malnutrition</li>
                <li>Social insurance</li>
                <li>Mortality rate</li>
                <li>Health Services</li>
              </UL>
              
              </p>
            </div>
          </div>
          <div class="col-md-4 py-3 py-md-0">
            <div class="card-service wow fadeInUp">
              <div class="circle-shape bg-primary text-white">
                <span>PT</span>
              </div>
              <p><span>PROTECTION</span>
                <UL style="background-color: white;font-size: 15px;">
                  <li>Child labour</li>
                  <li>Victim of armed conflict</li>
                  <li>Victim of sexual crimes</li>
                  <li>Restoring rights</li>
                  <li>Victims of psychoactive substances</li>
                </UL>
              </p>
            </div>
          </div>
          <div class="col-md-4 py-3 py-md-0">
            <div class="card-service wow fadeInUp">
              <div class="circle-shape bg-accent text-white">
                <span>DV</span>
              </div>
              <p><span>DEVELOPMENT</span>
                <UL style="background-color: white;font-size: 15px;">
                  <li>Education</li>
                  <li>ICBF attention</li>
                </UL></p>
            </div>
          </div>
        </div>
      </div>
    </div> <!-- .page-section -->

    <div class="page-section pb-0">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 py-3 wow fadeInUp" style="background-color: #2D3B38; ">
            <h1 style="color: white;">Abstract</h1>
            <p class="mb-4 " style="background-color: rgb(226, 226, 226);color: rgb(27, 6, 100);">The mayoralty needs to locate and quantify the number of children and teens in the 17 neighborhoods and 3 rural main areas of Bucaramanga. This allows the mayoralty to establish public policies between the future set of 23 policies they will implement during the next few years. Besides, visualizing changes of the trends of vulnerability before and after the pandemic is also desirable. Finally, the solution of this problem will be added to the digital observatory of the city.</p>
          </div>
          <div class="col-lg-6 wow fadeInRight" data-wow-delay="400ms">
            <div class="img-place custom-img-1">
              <img src="https://www.unicef.org/parenting/sites/unicef.org.parenting/files/3_Child_care.gif" alt="">
            </div>
          </div>
        </div>
      </div>
    </div> 
    <br>
    <div class="page-section pb-0">
      <div class="container">
        <div class="row align-items-center">
          <div class="col-lg-6 py-3 wow fadeInUp" style="color: rgb(27, 6, 100)">
            <h1>Data sources</h1>
          </div>
        </div>
      </div>
    </div>
      
    <br>
    <div class="bg-light">
      <div class="page-section py-3 mt-md-n5 custom-index">
        <div class="container">
          <div class="row">
            <div class="col-md-4 py-3 py-md-0">
              <div class="card-service wow fadeInUp">
                <p><span>SISBEN</span>
                  <UL style="background-color: white;font-size: 15px;">
                    <li>Social data of the Information System of Recipients of Social Programmes</li>
                  </UL>
                </p>
              </div>
            </div>
            
            <div class="col-md-4 py-3 py-md-0">
              <div class="card-service wow fadeInUp">
                <p><span>DANE</span>
                <UL style="background-color: white;font-size: 15px;">
                  <li>Gran encuesta hogares(GEIH)</li>
                  <li>Poverty Multidimensional Index(IPM)</li>
                  <li>National Population and Housing Census (CPNV)</li>
                </UL>
                
                </p>
              </div>
            </div>
            <div class="col-md-4 py-3 py-md-0">
              <div class="card-service wow fadeInUp">
                <p><span>Bucaramanga Mayoralty</span>
                  <UL style="background-color: white;font-size: 15px;">
                    <li>Enrollment in official educational institutions</li>
                  </UL></p>
              </div>
            </div>
            </div>
            <div class="row">
              <div class="col-md-4 py-3 py-md-0">
                <div class="card-service wow fadeInUp">
                  <p><span>Policía Nacional</span>
                  <UL style="background-color: white;font-size: 15px;">
                    <li>Crimes & sexual offence</li>
                  </UL>
                  
                  </p>
                </div>
              </div>
              <div class="col-md-8 py-3 py-md-0">
                <div class="card-service wow fadeInUp">
                  <p><span>Open Data Colombia</span>
                    <UL style="background-color: white;font-size: 15px;">
                      <li>Malnutrition heavy cases in children less than 5 years</li>
                      <li>Restoring rights (PARD) NNA</li>
                      <li>Gender violence</li>
                      <li>Affiliation to health services (EPS)</li>
                    </UL>
                  </p>
                </div>
              </div>
            </div>
          </div>
          
        </div>
      </div>
  </div>
  </div> 

  


  <footer class="page-footer">
    <div class="container">
      <div class="row px-md-3">
        <div class="col-sm-6 col-lg-3 py-3">
          <h5>DS4A</h5>
        </div>
        <div class="col-sm-6 col-lg-3 py-3">
          <h5>Alcaldía de bucaramanga</h5>
        </div>
        <div class="col-sm-12 col-lg-3 py-3">
          <h5>Septiembre 2021,Colombia</h5>
        </div>
      </div>
      <hr>
    </div>
  </footer>
  
</body>
</html>

    '''),
])
