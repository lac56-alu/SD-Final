/*
 * Simple Inventory API
 *
 * This is a simple API
 *
 * OpenAPI spec version: 1.0.0
 * Contact: lac56@gcloud.ua.es
 * Generated by: https://github.com/swagger-api/swagger-codegen.git
 */
using System;
using System.Linq;
using System.IO;
using System.Text;
using System.Collections;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.ComponentModel.DataAnnotations;
using System.Runtime.Serialization;
using Newtonsoft.Json;

namespace IO.Swagger.Models
{ 
    /// <summary>
    /// 
    /// </summary>
    [DataContract]
    public partial class InlineResponse200 : IEquatable<InlineResponse200>
    { 
        /// <summary>
        /// Gets or Sets Correcto
        /// </summary>

        [DataMember(Name="correcto")]
        public bool? Correcto { get; set; }

        /// <summary>
        /// Gets or Sets Cadena
        /// </summary>

        [DataMember(Name="cadena")]
        public string Cadena { get; set; }

        /// <summary>
        /// Gets or Sets Usuario
        /// </summary>

        [DataMember(Name="usuario")]
        public UserItem Usuario { get; set; }

        /// <summary>
        /// Returns the string presentation of the object
        /// </summary>
        /// <returns>String presentation of the object</returns>
        public override string ToString()
        {
            var sb = new StringBuilder();
            sb.Append("class InlineResponse200 {\n");
            sb.Append("  Correcto: ").Append(Correcto).Append("\n");
            sb.Append("  Cadena: ").Append(Cadena).Append("\n");
            sb.Append("  Usuario: ").Append(Usuario).Append("\n");
            sb.Append("}\n");
            return sb.ToString();
        }

        /// <summary>
        /// Returns the JSON string presentation of the object
        /// </summary>
        /// <returns>JSON string presentation of the object</returns>
        public string ToJson()
        {
            return JsonConvert.SerializeObject(this, Formatting.Indented);
        }

        /// <summary>
        /// Returns true if objects are equal
        /// </summary>
        /// <param name="obj">Object to be compared</param>
        /// <returns>Boolean</returns>
        public override bool Equals(object obj)
        {
            if (ReferenceEquals(null, obj)) return false;
            if (ReferenceEquals(this, obj)) return true;
            return obj.GetType() == GetType() && Equals((InlineResponse200)obj);
        }

        /// <summary>
        /// Returns true if InlineResponse200 instances are equal
        /// </summary>
        /// <param name="other">Instance of InlineResponse200 to be compared</param>
        /// <returns>Boolean</returns>
        public bool Equals(InlineResponse200 other)
        {
            if (ReferenceEquals(null, other)) return false;
            if (ReferenceEquals(this, other)) return true;

            return 
                (
                    Correcto == other.Correcto ||
                    Correcto != null &&
                    Correcto.Equals(other.Correcto)
                ) && 
                (
                    Cadena == other.Cadena ||
                    Cadena != null &&
                    Cadena.Equals(other.Cadena)
                ) && 
                (
                    Usuario == other.Usuario ||
                    Usuario != null &&
                    Usuario.Equals(other.Usuario)
                );
        }

        /// <summary>
        /// Gets the hash code
        /// </summary>
        /// <returns>Hash code</returns>
        public override int GetHashCode()
        {
            unchecked // Overflow is fine, just wrap
            {
                var hashCode = 41;
                // Suitable nullity checks etc, of course :)
                    if (Correcto != null)
                    hashCode = hashCode * 59 + Correcto.GetHashCode();
                    if (Cadena != null)
                    hashCode = hashCode * 59 + Cadena.GetHashCode();
                    if (Usuario != null)
                    hashCode = hashCode * 59 + Usuario.GetHashCode();
                return hashCode;
            }
        }

        #region Operators
        #pragma warning disable 1591

        public static bool operator ==(InlineResponse200 left, InlineResponse200 right)
        {
            return Equals(left, right);
        }

        public static bool operator !=(InlineResponse200 left, InlineResponse200 right)
        {
            return !Equals(left, right);
        }

        #pragma warning restore 1591
        #endregion Operators
    }
}
