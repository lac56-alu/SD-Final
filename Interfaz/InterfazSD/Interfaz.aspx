<%@ Page Async="true" Language="C#" AutoEventWireup="true" CodeBehind="Interfaz.aspx.cs" Inherits="InterfazSD.Interfaz" %>

<!DOCTYPE html>

<html xmlns="http://www.w3.org/1999/xhtml">
<head runat="server">
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title></title>
</head>
<body>
    <form id="form1" runat="server">

        <div>
            <h2>
                Mostrar Ciudades
            </h2>

            <asp:Button ID="mostrarCiudades" Text="Mostrar" runat="server" OnClick="MostrarCiudades" Width="103px" />
            </br></br>
            <h3><asp:Label id="MensajeMostrarCiudades" runat="server"/></h3>

        </div>
        
        </br></br>

        <div>
            <h2>
                Mostrar Temperaturas
            </h2>

            <asp:Button ID="mostrarTemperaturas" Text="Mostrar" runat="server" OnClick="MostrarTemperaturas" Width="103px" />
            </br></br>
            <h3><asp:Label id="MensajeMostrarTemperaturas" runat="server"/></h3>

        </div>

        </br></br>

        <div>
            <h2>
                 Mostrar Mapa
            </h2>

            <ul>
                <li>
                    <label for="nombreUsuario">Usuario: </label>
                    <asp:TextBox id="nombreUsuario_consultar" runat="server" />
                </li>
            </ul>

            <asp:Button ID="mostrarMapa" Text="Mostrar" runat="server" OnClick="MostrarMapa" Width="103px" style="height: 26px" />
            </br></br>
            <h3><asp:Label id="MensajeMostrarMapa" runat="server"/></h3>

        </div>

        <div>
            <h2>
                 Modificar Cuadrante
            </h2>

            <ul>
                <li>
                    <label for="posicion">Posicion: </label>
                    <asp:TextBox id="posicion_modificar" runat="server" />
                </li>
                <li>
                    <label for="nuevaCiudad">Ciudad Nueva: </label>
                    <asp:TextBox id="ciudad_modificar" runat="server" />
                </li>
            </ul>

            <asp:Button ID="modificarCuadrante" Text="Modificar" runat="server" OnClick="ModificarCuadrante" Width="103px" style="height: 26px" />
            </br></br>
            <h3><asp:Label id="MensajeModificarCuadrante" runat="server"/></h3>

        </div>

    </form>
</body>
</html>
