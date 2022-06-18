using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using System.Net.Http;
using System.Net.Http.Headers;
using System.Text;
using Newtonsoft.Json.Linq;

namespace InterfazSD
{
    public partial class Interfaz : System.Web.UI.Page
    {
        string ipAPI = "localhost";

        protected void Page_Load(object sender, EventArgs e)
        {

        }

        protected async void MostrarCiudades(object sender, EventArgs e)
        {
            try
            {
                var request = new HttpRequestMessage();
                string url = "http://" + ipAPI + ":50352/lac56-alu/SD-ENGINE/1.0.0/mostrarCiudades";
                request.RequestUri = new Uri(url);
                request.Method = HttpMethod.Get;

                var cliente = new HttpClient();
                HttpResponseMessage response = await cliente.SendAsync(request);
                string respuesta = await response.Content.ReadAsStringAsync();
                var json = JObject.Parse(respuesta)["cadena"];

                MensajeMostrarCiudades.Text = json.ToString();
            }
            catch (Exception exc)
            {
                MensajeMostrarCiudades.Text = exc.Message;
            }
        }

        protected async void MostrarTemperaturas(object sender, EventArgs e)
        {
            try
            {
                var request = new HttpRequestMessage();
                string url = "http://" + ipAPI + ":50352/lac56-alu/SD-ENGINE/1.0.0/mostrarTemperaturas";
                request.RequestUri = new Uri(url);
                request.Method = HttpMethod.Get;

                var cliente = new HttpClient();
                HttpResponseMessage response = await cliente.SendAsync(request);
                string respuesta = await response.Content.ReadAsStringAsync();
                var json = JObject.Parse(respuesta)["cadena"];

                MensajeMostrarTemperaturas.Text = json.ToString();
            }
            catch (Exception exc)
            {
                MensajeMostrarTemperaturas.Text = exc.Message;
            }
        }

        protected async void MostrarMapa(object sender, EventArgs e)
        {
            try
            {
                var request = new HttpRequestMessage();
                string url = "http://" + ipAPI + ":50352/lac56-alu/SD-ENGINE/1.0.0/mostrarMapa/" + nombreUsuario_consultar.Text;
                request.RequestUri = new Uri(url);
                request.Method = HttpMethod.Get;

                var cliente = new HttpClient();
                HttpResponseMessage response = await cliente.SendAsync(request);
                string respuesta = await response.Content.ReadAsStringAsync();
                var json = JObject.Parse(respuesta)["cadena"];

                MensajeMostrarMapa.Text = json.ToString();
            }
            catch (Exception exc)
            {
                MensajeMostrarMapa.Text = exc.Message;
            }
        }

        protected async void ModificarCuadrante(object sender, EventArgs e)
        {
            try
            {
                if ((posicion_modificar.Text == "0" || posicion_modificar.Text == "1" || posicion_modificar.Text == "2" || posicion_modificar.Text == "3") && ciudad_modificar.Text != "")
                {
                    var request = new HttpRequestMessage();
                    string url = "http://" + ipAPI + ":50352/lac56-alu/SD-ENGINE/1.0.0/modificarCuadrante/" + posicion_modificar.Text + "/" + ciudad_modificar.Text;
                    request.RequestUri = new Uri(url);
                    request.Method = HttpMethod.Put;

                    var cliente = new HttpClient();
                    HttpResponseMessage response = await cliente.SendAsync(request);
                    string respuesta = await response.Content.ReadAsStringAsync();
                    var json = JObject.Parse(respuesta)["cadena"];

                    MensajeModificarCuadrante.Text = json.ToString();
                }
                else
                {
                    MensajeModificarCuadrante.Text = "Introduce de forma correcta los paramentros";
                }

               
            }
            catch (Exception exc)
            {
                MensajeModificarCuadrante.Text = exc.Message;
            }
        }
    }
}