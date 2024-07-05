from datetime import datetime
import pytz


# Función para convertir la fecha al formato deseado
def convert_to_desired_format(iso_date):
    # Convertir la cadena de texto a un objeto datetime
    utc_time = datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")

    # Asignar la zona horaria UTC al objeto datetime
    utc_time = utc_time.replace(tzinfo=pytz.UTC)

    # Formatear la fecha y hora en el formato deseado
    formatted_time = utc_time.strftime("%Y-%m-%d %H:%M:%S.%f %z")

    # Ajustar el formato para incluir el separador de los dos puntos en la zona horaria
    formatted_time = formatted_time[:-2] + ":" + formatted_time[-2:]

    return formatted_time