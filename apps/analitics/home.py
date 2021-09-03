import dash_core_components as dcc
import dash_html_components as html
import dash_dangerously_set_inner_html
from dash.dependencies import Input, Output
import dash
import os
from app import app
import flask

url_back=app.get_asset_url('background1.png')

layout = html.Div([
    dash_dangerously_set_inner_html.DangerouslySetInnerHTML('''
        <style type="text/css">
<!--
span.cls_002{font-family:Arial,serif;font-size:44.5px;color:#00a899;font-weight:bold;font-style:normal;text-decoration: none}
div.cls_002{font-family:Arial,serif;font-size:44.5px;color:rgb(5,87,128);font-weight:bold;font-style:normal;text-decoration: none}
span.cls_003{font-family:Arial,serif;font-size:25.2px;color:rgb(255,255,255);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_003{font-family:Arial,serif;font-size:25.2px;color:rgb(255,255,255);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_004{font-family:Arial,serif;font-size:43.9px;color:#00a899;font-weight:bold;font-style:normal;text-decoration: none}
div.cls_004{font-family:Arial,serif;font-size:43.9px;color:rgb(239,93,45);font-weight:bold;font-style:normal;text-decoration: none}
span.cls_005{font-family:Arial,serif;font-size:28.1px;color:rgb(9,35,65);font-weight:bold;font-style:normal;text-decoration: none}
div.cls_005{font-family:Arial,serif;font-size:28.1px;color:rgb(9,35,65);font-weight:bold;font-style:normal;text-decoration: none}
span.cls_006{font-family:Arial,serif;font-size:20.9px;color:rgb(83,83,83);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_006{font-family:Arial,serif;font-size:20.9px;color:rgb(83,83,83);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_007{font-family:Arial,serif;font-size:26.1px;color:rgb(254,254,255);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_007{font-family:Arial,serif;font-size:26.1px;color:rgb(254,254,255);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_008{font-family:Arial,serif;font-size:14.6px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_008{font-family:Arial,serif;font-size:14.6px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_009{font-family:Arial,serif;font-size:21.9px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_009{font-family:Arial,serif;font-size:21.9px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_010{font-family:Arial,serif;font-size:11.6px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_010{font-family:Arial,serif;font-size:11.6px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_011{font-family:Arial,serif;font-size:32.0px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_011{font-family:Arial,serif;font-size:32.0px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_012{font-family:Arial,serif;font-size:29.0px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_012{font-family:Arial,serif;font-size:29.0px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_014{font-family:Arial,serif;font-size:13.5px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_014{font-family:Arial,serif;font-size:13.5px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
span.cls_013{font-family:Arial,serif;font-size:13.5px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
div.cls_013{font-family:Arial,serif;font-size:13.5px;color:rgb(0,0,0);font-weight:normal;font-style:normal;text-decoration: none}
-->
</style>

<div style="top:0px;width:100%;height:1190px;overflow:hidden;background-color:white">
<div style="position:absolute;left:0px;top:80px">
<img src="
'''
+url_back+
'''
" width=1683 height=1100></div>
<div style="position:absolute;left:550.70px;top:87.78px" class="cls_002"><span class="cls_002">Children and young vulnerability</span></div>
<div style="position:absolute;left:819.69px;top:316.28px" class="cls_003"><span class="cls_003">The mayoralty needs to locate and quantify the number of children</span></div>
<div style="position:absolute;left:819.69px;top:350.78px" class="cls_003"><span class="cls_003">and teens in the 17 neighborhoods and 3 rural main areas of</span></div>
<div style="position:absolute;left:204.43px;top:344.39px" class="cls_004"><span class="cls_004">Bucaramanga , Santander</span></div>
<div style="position:absolute;left:819.69px;top:385.29px" class="cls_003"><span class="cls_003">Bucaramanga. This allows the mayoralty to establish public policies</span></div>
<div style="position:absolute;left:819.69px;top:419.79px" class="cls_003"><span class="cls_003">between the future set of 23 policies they will implement during the</span></div>
<div style="position:absolute;left:819.69px;top:454.30px" class="cls_003"><span class="cls_003">next few years. Besides, visualizing changes of the trends of</span></div>
<div style="position:absolute;left:819.69px;top:488.80px" class="cls_003"><span class="cls_003">vulnerability before and after the pandemic is also desirable. Finally,</span></div>
<div style="position:absolute;left:819.69px;top:523.31px" class="cls_003"><span class="cls_003">the solution of this problem will be added to the digital observatory</span></div>
<div style="position:absolute;left:819.69px;top:557.81px" class="cls_003"><span class="cls_003">of the city.</span></div>
<div style="position:absolute;left:1063.86px;top:666.71px" class="cls_005"><span class="cls_005">INDEX COMPOSITION</span></div>
<div style="position:absolute;left:1069.02px;top:700.78px" class="cls_006"><span class="cls_006">fundamental rights - UNICEF</span></div>
<div style="position:absolute;left:915.12px;top:781.69px" class="cls_007"><span class="cls_007">SURVIVAL</span></div>
<div style="position:absolute;left:1146.49px;top:781.69px" class="cls_007"><span class="cls_007">PROTECTION</span></div>
<div style="position:absolute;left:1427.09px;top:781.69px" class="cls_007"><span class="cls_007">GROUTH</span></div>
<div style="position:absolute;left:1180.55px;top:823.32px" class="cls_008"><span class="cls_008">Child labour </span> </div>
<div style="position:absolute;left:911.37px;top:836.30px" class="cls_009"><span class="cls_009">Malnutrition</span></div>
<div style="position:absolute;left:1142.83px;top:842.82px" class="cls_008"><span class="cls_008">Victim of armed conflict</span></div>
<div style="position:absolute;left:1427.70px;top:835.96px" class="cls_009"><span class="cls_009">Education</span></div>
<div style="position:absolute;left:1145.52px;top:862.32px" class="cls_008"><span class="cls_008">Victim of sexual crimes</span></div>
<div style="position:absolute;left:891.24px;top:865.55px" class="cls_009"><span class="cls_009">Social insurance</span></div>
<div style="position:absolute;left:1407.50px;top:865.21px" class="cls_009"><span class="cls_009">ICBF attention</span></div>
<div style="position:absolute;left:1169.16px;top:881.83px" class="cls_008"><span class="cls_008">Restoring rights</span></div>
<div style="position:absolute;left:905.72px;top:894.81px" class="cls_009"><span class="cls_009">Mortality rate</span></div>
<div style="position:absolute;left:1104.16px;top:901.33px" class="cls_008"><span class="cls_008">Victims of </span>psychoactive substances</div>
<div style="position:absolute;left:1110.06px;top:920.83px" class="cls_010"><span class="cls_010">(distribution,production and consumption)</span></div>
<div style="position:absolute;left:148.13px;top:1059.42px" class="cls_011"><span class="cls_011">SISBEN</span></div>
<div style="position:absolute;left:551.79px;top:1059.42px" class="cls_011"><span class="cls_011">DANE</span></div>
<div style="position:absolute;left:933.14px;top:1064.08px" class="cls_012"><span class="cls_012">Open Data Colombia</span></div>
<div style="position:absolute;left:1369.50px;top:1059.42px" class="cls_011"><span class="cls_011">Policía Nacional</span></div>
<div style="position:absolute;left:148.13px;top:1107.80px" class="cls_014"><span class="cls_014"> </span><A HREF="https://www.sisben.gov.co/Paginas/que-es-sisben.aspx">Social data of the Information System of</A> </div>
<div style="position:absolute;left:551.79px;top:1107.80px" class="cls_014"><span class="cls_014">Gran encuesta horages (GEIH </span><span class="cls_013">) / </span></div>
<div style="position:absolute;left:933.14px;top:1108.93px" class="cls_013"><span class="cls_013">Malnutrition</span></div>
<div style="position:absolute;left:1369.50px;top:1107.80px" class="cls_014"><span class="cls_014"> </span><A HREF="https://www.policia.gov.co/grupo-informacion-criminalidad/estadistica-delictiva">Crimes & sexual offence</A> </div>
<div style="position:absolute;left:148.13px;top:1126.55px" class="cls_014"><span class="cls_014"> </span><A HREF="https://www.sisben.gov.co/Paginas/que-es-sisben.aspx">Recipients of Social Programmes</A> </div>
<div style="position:absolute;left:551.79px;top:1126.55px" class="cls_014"><span class="cls_014">Poverty Multidimensional Index(IPM)</span><span class="cls_013"> / </span></div>
<div style="position:absolute;left:933.14px;top:1127.68px" class="cls_013"><A HREF="https://www.datos.gov.co/Inclusi-n-Social-y-Reconciliaci-n/Ingresos-a-Procesos-Administrativos-de-Restablecim/gj35-hct5">Restoring rights (PARD) NNA</A><span class="cls_013"> /  </div>
<div style="position:absolute;left:551.79px;top:1145.30px" class="cls_014"><span class="cls_014"> </span><A HREF="http://microdatos.dane.gov.co/index.php/catalog/643">National Population and Housing Census (CPNV)</A> </div>
<div style="position:absolute;left:933.14px;top:1146.43px" class="cls_013"></span><A HREF="https://www.datos.gov.co/Salud-y-Protecci-n-Social/Violencia-de-G-nero/sq8q-pnf5">Gender Violence</A> </span></div>
</div>

    '''),
])
