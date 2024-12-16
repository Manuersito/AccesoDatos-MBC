import logging
import mysql.connector
from mysql.connector import Error

# Configuración de logging para guardar en un archivo
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("log_datos_bd.log"),
    ]
)

class DataManagerDB:
    def __init__(self, host, user, password, database, tabla="Moviles"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.tabla = tabla
        self.connection = None
        self.transaccion_activa = False

        # Conectar a la base de datos al inicializar el gestor
        self._conectar()
        self._crear_tabla_si_no_existe()

    def _conectar(self):
        """Establecer conexión a la base de datos."""
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.connection.autocommit = False  # Desactiva autocommit para manejar transacciones
                logging.info("Conexión establecida con la base de datos.")
        except Error as e:
            logging.error(f"Error al conectar a la base de datos: {e}")
            raise

    def _crear_tabla_si_no_existe(self):
        """Crear la tabla 'Moviles' si no existe."""
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"""
                CREATE TABLE IF NOT EXISTS {self.tabla} (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    marca VARCHAR(50),
                    modelo VARCHAR(50),
                    sistema_operativo VARCHAR(50),
                    capacidad INT,
                    precio DECIMAL(10, 2),
                    tienda_id INT
                )
            """)
            logging.info(f"Tabla '{self.tabla}' creada o ya existente.")
        except Error as e:
            logging.error(f"Error al crear la tabla '{self.tabla}': {e}")
            raise

    def iniciar_transaccion(self):
        """Iniciar una transacción."""
        if self.transaccion_activa:
            raise Exception("Ya hay una transacción activa.")
        self.transaccion_activa = True
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        """Confirmar la transacción actual."""
        if not self.transaccion_activa:
            raise Exception("No hay transacción activa para confirmar.")
        try:
            self.connection.commit()
            self.transaccion_activa = False
            logging.info("Transacción confirmada.")
        except Error as e:
            logging.error(f"Error al confirmar la transacción: {e}")
            self.revertir_transaccion()

    def revertir_transaccion(self):
        """Revertir la transacción actual."""
        if not self.transaccion_activa:
            raise Exception("No hay transacción activa para revertir.")
        try:
            self.connection.rollback()
            self.transaccion_activa = False
            logging.warning("Transacción revertida.")
        except Error as e:
            logging.error(f"Error al revertir la transacción: {e}")

    def escribir_dato(self, movil):
        """Insertar un móvil en la tabla."""
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        try:
            cursor = self.connection.cursor()
            query = f"""
                INSERT INTO {self.tabla} (marca, modelo, sistema_operativo, capacidad, precio, tienda_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (movil['marca'], movil['modelo'], movil['sistema_operativo'],
                                   movil['capacidad'], movil['precio'], movil['tienda_id']))
            logging.info(f"Móvil agregado: {movil}")
        except Error as e:
            logging.error(f"Error al agregar el móvil: {e}")
            raise

    def leer_dato(self, clave, valor):
        """Leer móviles según un filtro."""
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = f"SELECT * FROM {self.tabla} WHERE {clave} = %s"
            cursor.execute(query, (valor,))
            resultados = cursor.fetchall()
            logging.info(f"Datos leídos: {resultados}")
            return resultados
        except Error as e:
            logging.error(f"Error al leer datos: {e}")
            raise

    def eliminar_dato(self, clave, valor):
        """Eliminar móviles según un filtro."""
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        try:
            cursor = self.connection.cursor()
            query = f"DELETE FROM {self.tabla} WHERE {clave} = %s"
            cursor.execute(query, (valor,))
            logging.info(f"Datos eliminados con {clave}={valor}.")
        except Error as e:
            logging.error(f"Error al eliminar datos: {e}")
            raise

    def cerrar(self):
        """Cerrar conexión a la base de datos."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Conexión cerrada.")

# Ejemplo de uso con datos de móviles
def main():
    # Crear el gestor de datos
    db_manager = DataManagerDB(
        host="localhost",
        user="usuario",
        password="usuario",
        database="1dam"
    )

    try:
        # Iniciar una transacción
        db_manager.iniciar_transaccion()

        # Agregar un móvil
        nuevo_movil = {
            "marca": "Samsung",
            "modelo": "Galaxy S23",
            "sistema_operativo": "Android",
            "capacidad": 128,
            "precio": 899.99,
            "tienda_id": 1
        }
        db_manager.escribir_dato(nuevo_movil)

        # Confirmar la transacción
        db_manager.confirmar_transaccion()

        # Leer móviles con un filtro
        resultados = db_manager.leer_dato("marca", "Samsung")
        print("Resultados de lectura:", resultados)

        # Iniciar otra transacción para eliminar
        db_manager.iniciar_transaccion()
        db_manager.eliminar_dato("modelo", "Mi 11")
        db_manager.confirmar_transaccion()
    finally:
        db_manager.cerrar()

if __name__ == "__main__":
    main()
