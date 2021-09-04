import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import dash
import dash_dangerously_set_inner_html

from app import app

layout = html.Div([
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML(f"""
    <!DOCTYPE html>
<html style="font-size: 16px;">
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="utf-8">
    <meta name="keywords" content="Our Team">
    <meta name="description" content="">
    <meta name="page_type" content="np-template-header-footer-from-plugin">
    <title>Home</title>
    <link rel="stylesheet" href="""+app.get_asset_url('static_pages/nicepage.css')+""" media="screen">
    <link rel="stylesheet" href="""+app.get_asset_url('static_pages/Home.css')+""" media="screen">
    <!-- <script class="u-script" type="text/javascript" src="jquery.js" defer=""></script> -->
    <!-- <script class="u-script" type="text/javascript" src="nicepage.js" defer=""></script> -->
    <meta name="generator" content="Nicepage 3.24.3, nicepage.com">
    <link id="u-theme-google-font" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:100,100i,300,300i,400,400i,500,500i,700,700i,900,900i|Open+Sans:300,300i,400,400i,600,600i,700,700i,800,800i">
    <link id="u-page-google-font" rel="stylesheet" href="https://fonts.googleapis.com/css?family=Oswald:200,300,400,500,600,700">
    
    
    <script type="application/ld+json">{
		"@context": "http://schema.org",
		"@type": "Organization",
		"name": "",
		"logo": "images/default-logo.png"
}</script>
    <meta name="theme-color" content="#478ac9">
    <meta property="og:title" content="Home">
    <meta property="og:type" content="website">
  </head>
  <body data-home-page="Home.html" data-home-page-title="Home" class="u-body">
    <section class="u-align-center u-clearfix u-section-1" id="carousel_ace9">
      <div class="u-clearfix u-sheet u-sheet-1">
        <!-- <h1 class="u-custom-font u-font-oswald u-text u-text-default u-text-palette-2-base u-text-1">Our Team</h1>
        <p class="u-text u-text-default u-text-2">Glavrida for habitant morbi tristique senectus et netus et malesuada fames</p> -->
        <div class="u-expanded-width u-list u-list-1">
          <div class="u-repeater u-repeater-1">
            <div class="u-align-center u-container-style u-list-item u-repeater-item u-white u-list-item-1">
              <div class="u-container-layout u-similar-container u-valign-top u-container-layout-1">
                <div alt="" class="u-image u-image-circle u-image-1" data-image-width="598" data-image-height="598"></div>
                <h3 class="u-align-center u-custom-font u-font-oswald u-text u-text-3">Angye Katherine Malagon </h3>
                <p class="u-align-center u-text u-text-palette-1-base u-text-4">Systems engineer</p>
                <div class="u-social-icons u-spacing-10 u-social-icons-1">
                  <a class="u-social-url" target="_blank" href="mailto:angyemala@gmail.com"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-1" style="margin: 14px auto 0; font-size: 200%; color: black">&#9993;</span> 
                  </a>
                  <a class="u-social-url" target="_blank" href="https://www.linkedin.com/in/angyemalagon-b2700673/"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-4"><svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 112 112" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-78e1"></use></svg><svg x="0px" y="0px" viewBox="0 0 112 112" id="svg-78e1" class="u-svg-content"><path d="M33.8,96.8H14.5v-58h19.3V96.8z M24.1,30.9L24.1,30.9c-6.6,0-10.8-4.5-10.8-10.1c0-5.8,4.3-10.1,10.9-10.1 S34.9,15,35.1,20.8C35.1,26.4,30.8,30.9,24.1,30.9z M103.3,96.8H84.1v-31c0-7.8-2.7-13.1-9.8-13.1c-5.3,0-8.5,3.6-9.9,7.1 c-0.6,1.3-0.6,3-0.6,4.8V97H44.5c0,0,0.3-52.6,0-58h19.3v8.2c2.6-3.9,7.2-9.6,17.4-9.6c12.7,0,22.2,8.4,22.2,26.1V96.8z"></path></svg></span>
                  </a>
                </div>
              </div>
            </div><div class="u-align-center u-container-style u-list-item u-repeater-item u-white u-list-item-1">
              <div class="u-container-layout u-similar-container u-valign-top u-container-layout-1">
                <div alt="" class="u-image u-image-circle u-image-2" data-image-width="598" data-image-height="598"></div>
                <h3 class="u-align-center u-custom-font u-font-oswald u-text u-text-3">Aurelio Esquivia Lopez </h3>
                <p class="u-align-center u-text u-text-palette-1-base u-text-4">Chemical engineer</p>
                <div class="u-social-icons u-spacing-10 u-social-icons-1">
                  <a class="u-social-url" target="_blank" href="mailto:aesquivial@unicartagena.edu.co"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-1" style="margin: 14px auto 0; font-size: 200%; color: black">&#9993;</span> 
                  </a>
                  <a class="u-social-url" target="_blank" href="https://www.linkedin.com/in/aurelio-esquivia-lopez-75964ba8/"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-4"><svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 112 112" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-78e1"></use></svg><svg x="0px" y="0px" viewBox="0 0 112 112" id="svg-78e1" class="u-svg-content"><path d="M33.8,96.8H14.5v-58h19.3V96.8z M24.1,30.9L24.1,30.9c-6.6,0-10.8-4.5-10.8-10.1c0-5.8,4.3-10.1,10.9-10.1 S34.9,15,35.1,20.8C35.1,26.4,30.8,30.9,24.1,30.9z M103.3,96.8H84.1v-31c0-7.8-2.7-13.1-9.8-13.1c-5.3,0-8.5,3.6-9.9,7.1 c-0.6,1.3-0.6,3-0.6,4.8V97H44.5c0,0,0.3-52.6,0-58h19.3v8.2c2.6-3.9,7.2-9.6,17.4-9.6c12.7,0,22.2,8.4,22.2,26.1V96.8z"></path></svg></span>
                  </a>
                </div>
              </div>
            </div><div class="u-align-center u-container-style u-list-item u-repeater-item u-white u-list-item-1">
              <div class="u-container-layout u-similar-container u-valign-top u-container-layout-1">
                <div alt="" class="u-image u-image-circle u-image-3" data-image-width="598" data-image-height="598"></div>
                <h3 class="u-align-center u-custom-font u-font-oswald u-text u-text-3">Betty Jazmín Gutiérrez</h3>
                <p class="u-align-center u-text u-text-palette-1-base u-text-4">M.Sc Agricultural engineering</p>
                <div class="u-social-icons u-spacing-10 u-social-icons-1">
                  <a class="u-social-url" target="_blank" href="mailto:bjgutierrez@agrosavia.co"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-1" style="margin: 14px auto 0; font-size: 200%; color: black">&#9993;</span> 
                  </a>
                  <a class="u-social-url" target="_blank" href="https://www.linkedin.com/in/jazmingutierrezr/"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-4"><svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 112 112" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-78e1"></use></svg><svg x="0px" y="0px" viewBox="0 0 112 112" id="svg-78e1" class="u-svg-content"><path d="M33.8,96.8H14.5v-58h19.3V96.8z M24.1,30.9L24.1,30.9c-6.6,0-10.8-4.5-10.8-10.1c0-5.8,4.3-10.1,10.9-10.1 S34.9,15,35.1,20.8C35.1,26.4,30.8,30.9,24.1,30.9z M103.3,96.8H84.1v-31c0-7.8-2.7-13.1-9.8-13.1c-5.3,0-8.5,3.6-9.9,7.1 c-0.6,1.3-0.6,3-0.6,4.8V97H44.5c0,0,0.3-52.6,0-58h19.3v8.2c2.6-3.9,7.2-9.6,17.4-9.6c12.7,0,22.2,8.4,22.2,26.1V96.8z"></path></svg></span>
                  </a>
                </div>
              </div>
            </div><div class="u-align-center u-container-style u-list-item u-repeater-item u-white u-list-item-1">
              <div class="u-container-layout u-similar-container u-valign-top u-container-layout-1">
                <div alt="" class="u-image u-image-circle u-image-4" data-image-width="598" data-image-height="598"></div>
                <h3 class="u-align-center u-custom-font u-font-oswald u-text u-text-3">Esteban Palacio</h3>
                <p class="u-align-center u-text u-text-palette-1-base u-text-4">Software engineer</p>
                <div class="u-social-icons u-spacing-10 u-social-icons-1">
                  <a class="u-social-url" target="_blank" href="mailto:epalaciol@unal.edu.co"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-1" style="margin: 14px auto 0; font-size: 200%; color: black">&#9993;</span> 
                  </a>
                  <a class="u-social-url" target="_blank" href="https://www.linkedin.com/in/estebanpalaciol/"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-4"><svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 112 112" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-78e1"></use></svg><svg x="0px" y="0px" viewBox="0 0 112 112" id="svg-78e1" class="u-svg-content"><path d="M33.8,96.8H14.5v-58h19.3V96.8z M24.1,30.9L24.1,30.9c-6.6,0-10.8-4.5-10.8-10.1c0-5.8,4.3-10.1,10.9-10.1 S34.9,15,35.1,20.8C35.1,26.4,30.8,30.9,24.1,30.9z M103.3,96.8H84.1v-31c0-7.8-2.7-13.1-9.8-13.1c-5.3,0-8.5,3.6-9.9,7.1 c-0.6,1.3-0.6,3-0.6,4.8V97H44.5c0,0,0.3-52.6,0-58h19.3v8.2c2.6-3.9,7.2-9.6,17.4-9.6c12.7,0,22.2,8.4,22.2,26.1V96.8z"></path></svg></span>
                  </a>
                </div>
              </div>
            </div>
            <div class="u-align-center u-container-style u-list-item u-repeater-item u-white u-list-item-2">
              <div class="u-container-layout u-similar-container u-valign-top u-container-layout-2">
                <div alt="" class="u-image u-image-circle u-image-5"></div>
                <h3 class="u-align-center u-custom-font u-font-oswald u-text u-text-6">Jaime Andres Molina</h3>
                <p class="u-align-center u-text u-text-palette-1-base u-text-7">Statistician</p>
                <div class="u-social-icons u-spacing-10 u-social-icons-1">
                  <a class="u-social-url" target="_blank" href="mailto:jaamolinaco@unal.edu.co"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-1" style="margin: 14px auto 0; font-size: 200%; color: black">&#9993;</span> 
                  </a>
                  <a class="u-social-url" target="_blank" href="https://www.linkedin.com/in/jaimeandres-m/"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-8"><svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 112 112" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-78e1"></use></svg><svg x="0px" y="0px" viewBox="0 0 112 112" id="svg-78e1" class="u-svg-content"><path d="M33.8,96.8H14.5v-58h19.3V96.8z M24.1,30.9L24.1,30.9c-6.6,0-10.8-4.5-10.8-10.1c0-5.8,4.3-10.1,10.9-10.1 S34.9,15,35.1,20.8C35.1,26.4,30.8,30.9,24.1,30.9z M103.3,96.8H84.1v-31c0-7.8-2.7-13.1-9.8-13.1c-5.3,0-8.5,3.6-9.9,7.1 c-0.6,1.3-0.6,3-0.6,4.8V97H44.5c0,0,0.3-52.6,0-58h19.3v8.2c2.6-3.9,7.2-9.6,17.4-9.6c12.7,0,22.2,8.4,22.2,26.1V96.8z"></path></svg></span>
                  </a>
                </div>
              </div>
            </div>
            <div class="u-align-center u-container-style u-list-item u-repeater-item u-white u-list-item-3">
              <div class="u-container-layout u-similar-container u-valign-top u-container-layout-3">
                <div alt="" class="u-image u-image-circle u-image-6"></div>
                <h3 class="u-align-center u-custom-font u-font-oswald u-text u-text-9">Juan Jose Gomez</h3>
                <p class="u-align-center u-text u-text-palette-1-base u-text-10">Physicist</p>
                <div class="u-social-icons u-spacing-10 u-social-icons-1">
                  <a class="u-social-url" target="_blank" href="mailto:jujgomezro@unal.edu.co"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-1" style="margin: 14px auto 0; font-size: 200%; color: black">&#9993;</span> 
                  </a>  
                  <a class="u-social-url" target="_blank" href="https://www.linkedin.com/in/jujgomezro25/"><span class="u-icon u-icon-circle u-social-icon u-social-linkedin u-icon-1"><svg class="u-svg-link" preserveAspectRatio="xMidYMin slice" viewBox="0 0 112 112" style=""><use xmlns:xlink="http://www.w3.org/1999/xlink" xlink:href="#svg-78e1"></use></svg><svg x="0px" y="0px" viewBox="0 0 112 112" id="svg-78e1" class="u-svg-content"><path d="M33.8,96.8H14.5v-58h19.3V96.8z M24.1,30.9L24.1,30.9c-6.6,0-10.8-4.5-10.8-10.1c0-5.8,4.3-10.1,10.9-10.1 S34.9,15,35.1,20.8C35.1,26.4,30.8,30.9,24.1,30.9z M103.3,96.8H84.1v-31c0-7.8-2.7-13.1-9.8-13.1c-5.3,0-8.5,3.6-9.9,7.1 c-0.6,1.3-0.6,3-0.6,4.8V97H44.5c0,0,0.3-52.6,0-58h19.3v8.2c2.6-3.9,7.2-9.6,17.4-9.6c12.7,0,22.2,8.4,22.2,26.1V96.8z"></path></svg></span>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </body>
</html>""")
])