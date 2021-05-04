import time
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import psycopg2


class ActaServicio(models.Model):
    _name = 'acta.servicio'
    _description = 'Acta de servicio'
    #_order = 'desc, name'

    #Sección de reconocimiento de usuario actual
    current_user = fields.Integer('acta.servicio', default=lambda self: self.env.user.id)

    #validar que tipo de trabajo es.
    area_pt= fields.Selection([('pt1', 'Proyectos'), ('pt2', 'Mantenimiento')],
                                          string='¿El trabajo a realizar es un proyectos o mantenimiento?',
                                          required=True)


    #author_ids = fields.Many2one('res.partner', string='técnico', required=True)
    name = fields.Char('Numero de acta', required=False)  #
    #el orden de las variables va por el desarrollo del formulario

    #datos arrastrados
    tecnico_acta = fields.Char('Tecnico asignado', required=False)
    entidad_acta = fields.Char('Cliente', required=False)
    ciudad_acta = fields.Char('Ciudad', required=False)
    falla_reportada_acta = fields.Text('Falla reportada', required=False)
    falla_reportada_proyecto = fields.Html()
    codigo_acta = fields.Char('Codigo', required=False)
    codigo_acta_tipo = fields.Char('Codigo', required=False)
    codigo_acta_nombre = fields.Char('Codigo', required=False)
    hora_inicio_acta = fields.Datetime('Date current action', required=False, readonly=False, select=True, default=lambda self: fields.datetime.now())
    hora_final_acta = fields.Datetime('Date current action', required=True, readonly=False, select=True)
    #paso 1
    Servicio_inmediato = fields.Selection([('Si', 'Si se puede realizar'), ('No', 'No se puede realizar')],
                                          string='¿El servicio se puede realizar inmediatamente?',
                                          )
    #en caso de que se seleccione NO
    Motivos_no = fields.Selection(
        [('seleccione', 'Seleccione'),
         ('f1', 'Funcionario no puede atender al tecnico'),
         ('f2', 'Funcionario no se encuentra en la sucursal'),
         ('f3','Horario restringido'),
         ('f4','No hubo correo de permiso de ingreso'),
         ('f5','No se puede realizar inmediatamente'),
         ('f6','Operador central desconoce servio a Ejecutar'),
         ('f7','Operador central no contesta llamada'),
         ('f8','Operador global no contesta llamada'),
         ('f9','Otro proveedor no hace presencia en el sitio'),
         ('f10','Panel de alarma dentro de la scucursal'),
         ('f11','Proveedor no apertura otros cajeros'),
         ('f12','Proveedor no lleva llaves'),
         ('f13','Se requiere curso de seguridad industrial'),
         ('f14','Sin permiso de ingreso para otro proveedor'),
         ('f15','Sucursal con alto flujo de usuarios'),
         ('f16','Tecnico no alcanza a llegar'),
         ('f17','Transportadora no hace presencia en el sitio')],
        'Motivo por el cual no se puede realizar:', default="seleccione")
    SePuedeFirmar = fields.Selection([('Si', 'Si'), ('No', 'No')],
                                          string='¿Hay un funcionario que pueda firmar el acta?', required=True, default='No')
    notes = fields.Text('Observaciones del proceso', default="null")
    #fin del caso

    #En caso de que sea si
    Tipo_mantenimiento = fields.Selection([('t1', '¿TRABAJÓ EN SISTEMAS ELECTRÓNICOS?'),
                                           ('t2', '¿TRABAJÓ EN SISTEMAS METALMECÁNICOS?')],
                                            required=True, default='t1')
    #Sistemas electronicos
    Componente_trabajo = fields.Many2many('tipo.mantenimiento',required=False)
    Subsistema1 = fields.Selection(
        [('st1', 'Unidad central de proceso, elementos de salida o elementos energéticos')],
        'Seleccione el subsistema de alarma ')
    Subsistema2 = fields.Selection(
        [('cs1', 'Elementos de entrada')],
        'en el que trabajó')
    #campo relacionado con la clase de abajo
    Field_many2one = fields.Many2many('material.acta','materiales',required=False)
    prueba2 =fields.Many2one('maintenance.request', 'Seleccione el número de servicio')
    datosproyecto = fields.Many2one('project.project', string='Seleccione el número de servicio')

    #Alarma
    materiales_video = fields.Many2one('video.electronico')
    cantidad = fields.Integer('cantidad')

    trabajo_fin = fields.Selection([('Si', 'Si'), ('No', 'No')],
                                     string='¿Hay un funcionario que pueda firmar el acta?')

    # tabla para suministros de video electrónico
    campos = fields.One2many('video.electronico', 'appuesto')
    # tabla para suministros de alarma
    campos2 = fields.One2many('suministros.alarma','opuesto',)
    # tabla para suministros de video
    campos3 = fields.One2many('video.mano','opuesto',)
    #tabla para suministros de control de acceso
    campos4 = fields.One2many('control.acceso','opuesto',)
    #tabla de seleccion de actividades
    actividadesproyecto1 = fields.One2many('actividades_proyectos', 'opuesto')
    #Campo para la firma
    Firma = fields.Binary('')

    # datos de finalización
    observaciones_generales = fields.Text(default=" ")

    #variables para equipo metalmecánico

    campos1_metalmecanico = fields.One2many('equipo.liviano', 'opuesto', )
    campos2_metalmecanico = fields.One2many('equipo.pesado', 'opuesto', )
    campos3_metalmecanico = fields.One2many('suministros_metalmecanicos', 'opuesto', )

    xentero = fields.Integer()
    # variables para proyectos
    #Listaactividades = fields.Many2many('project.project', store=True, string='datos')


    #funciones
    # codigo de limpieza
    @api.onchange('area_pt')
    def _funcion_limpiar(self):
        if self.area_pt:
            if self.tecnico_acta != '':
                if self.area_pt == 'pt1':
                    print('Limpiar')
                    self.tecnico_acta = ''
                    self.entidad_acta = ''
                    self.ciudad_acta = ''
                    self.falla_reportada_acta = ''
                    self.codigo_acta = ''
                    self.codigo_acta_nombre = ''
                    self.codigo_acta_tipo = ''
                    self.falla_reportada_proyecto = ''



    @api.constrains('notes')
    @api.one
    def _check_your_field(self):
        if len(self.notes) > 1200:
            raise ValidationError('El número de caracteres no puede exceder los 1200')

    @api.constrains('observaciones_generales')
    @api.one
    def _ob_generales(self):
        if len(self.observaciones_generales) > 1200:
            raise ValidationError('El número de caracteres no puede exceder los 1200')
    #Codigo de opcion en caso dado que odoo no permita interacciones con la bd
    # @api.constrains('trabajo_fin')
    # @api.one
    # def _ob_generales(self):
    #     if self.trabajo_fin == 'Si':
    #         # x = self.prueba2.id
    #         # x = str(x)
    #         En esta parte toca ingresa el nombre de la base da datos en caso que se use y la base de datos sea cambiada
    #         conexion1 = psycopg2.connect(database="odoo_prueba", user="odoo", password="admin")
    #         cursor1 = conexion1.cursor()
    #         # comando = str("update maintenance_request set validador='TRUE' where id='"+x+"'")
    #         cursor1.execute("update maintenance_request set validador='TRUE' where id='"+str(self.prueba2.id)+"'")
    #         conexion1.commit()
    #         print(cursor1)
    # funcion para traer datos de proyectos

    @api.onchange('datosproyecto')
    def _onchange_proyecto(self):
        if self.datosproyecto:
            self.tecnico_acta = self.datosproyecto.enidadproyecto.name
            self.falla_reportada_proyecto = self.datosproyecto.informacion
            self.xentero = self.datosproyecto.id
            print(str(self.xentero))



    # esta funcion es la que arrastra los datos seleccionados en prueba2 que es igual a llamar el numero de servicio
    @api.onchange('prueba2')
    def _onchange_city_id(self):
        if self.prueba2:
            print('hola we')
            self.tecnico_acta = self.prueba2.user_id.name
            self.entidad_acta = self.prueba2.partner_id.name
            self.ciudad_acta = self.prueba2.city_id.name
            self.falla_reportada_acta = self.prueba2.description
            self.codigo_acta = self.prueba2.location_id.code
            self.codigo_acta_nombre = self.prueba2.location_id.name
            self.codigo_acta_tipo = self.prueba2.location_id.location_type_id.name
            self.prueba2.validador = True
            print(self.prueba2.validador)



# codigo creado por Efrain
    @api.constrains('trabajo_fin')
    @api.one
    def _validador(self):
        if self.trabajo_fin == 'Si':
            query = "UPDATE maintenance_request SET validador='TRUE' WHERE id='"+str(self.prueba2.id)+"'"
            self._cr.execute(query)
            self._cr.commit()
###########################no se puede eliminar##########################->
class material_acta(models.Model):
 #clase diseñada para integral el listado de SUBSISTEMA DE ALARMA EN EL QUE TRABAJÓ
    _name = 'material.acta'
    _rec_name='Nom_material'
    Nom_material = fields.Char('prueba', required=True)

class tipo_mantenimiento(models.Model):
    _name = 'tipo.mantenimiento'
    _rec_name = 'nombre_proceso'
    nombre_proceso = fields.Char('prueba', required=True)
###########################no se puede eliminar##########################<-
class materiales_video_electronicos(models.Model):
    _name = 'video.electronico'
    _rec_name = 'nombre'
    nombre = fields.Many2one('materiales.alarma', required=True)
    categoria = fields.Char('Categoria')
    observacion = fields.Many2many('mano.obra', string='Mano de obra')
    zona = fields.Char('¿PERTENECE A UNA ZONA O UBICACIÓN EN ESPECIAL SOBRE LA UCP?')
    cobertura = fields.Char('¿CUBRE UN ÁREA ESPECÍFICA?')
    placa = fields.Char('Placa')
    img = fields.Binary('Soporte visual')
    segunda_placa = fields.Char('Serial del elemento desmontado')
    img2 = fields.Binary('Soporte visual')
    appuesto = fields.Many2one('acta.servicio', string="", readonly="True")

    @api.onchange('nombre')
    def _onchange_city_id(self):
        if self.nombre:
            if self.nombre.grupo == 't1':
                self.categoria = 'UNIDAD CENTRAL DE PROCESO, ELEMENTOS DE SALIDA O ELEMENTOS ENERGÉTICOS'
            elif self.nombre.grupo == 't2':
                self.categoria = 'ELEMENTOS DE ENTRADA'
            elif self.nombre.grupo == 't3':
                self.categoria = 'N/A'

  #clase para el funcionamiento de las actividades
class actividades_proyectos(models.Model):
    _name = 'actividades_proyectos'
    Listaactividades = fields.Many2one('project.task', store=True, string='Actividad a realizar')
    Diaactividad = fields.Char('Dia al que pertenece la actividad')
    observacion = fields.Text('Comentarios')
    img = fields.Binary('Soporte visual')
    opuesto = fields.Many2one('acta.servicio', string="", readonly="True")
    xent = fields.Integer()

    def ejecutar(self):
        self.xent = self.opuesto.xentero
        print(str(self.xent))

    @api.onchange('Listaactividades')
    def _onchange_city_id(self):
        if self.Listaactividades:
           self.Diaactividad = self.Listaactividades.stage_id.name

class materiales_alarma(models.Model):
    _name = 'materiales.alarma'
    _rec_name = 'nombre'

    nombre = fields.Char('Nombre del equipo', required=True)
    grupo = fields.Selection([('t1', 'UNIDAD CENTRAL DE PROCESO, ELEMENTOS DE SALIDA O ELEMENTOS ENERGÉTICOS'),
                            ('t2', 'ELEMENTOS DE ENTRADA'),
                              ('t3','N/A')],
                            required=True)

class suministros_alarma(models.Model):
    _name = 'suministros.alarma'
    _rec_name = 'lista_cliente'
    lista_cliente = fields.Many2one('lista.clientes',
                                    string='Lista dada por el cliente, si requiere otro elemento comunicarse con el supervisor')
    cantidad = fields.Integer('cantidad')
    elementocambiado = fields.Selection([('r1', 'ENTREGADO'),
                                         ('r2', 'CAMBIADO')], string='EL ELEMENTO FUE:')
    # en caso dado que sea cambiado
    propiedad_material = fields.Selection([('r1', 'El cliente'),
                                           ('r2', 'El proveedor')
                                           ], string='El elemento cambiado es propiedad de:')
    indicaciones_material = fields.Selection([('r1', 'Nuevo'),
                                              ('r2', 'Usado')
                                              ], string='El elemento es:')
    opuesto = fields.Many2one('acta.servicio', string="", readonly="True")

class lista_clientes(models.Model):

    _name = 'lista.clientes'
    _rec_name = 'producto_lista'
    producto_lista = fields.Char('Iten que desea agregar', required=True)

class mano_obra(models.Model):
    _name = 'mano.obra'
    _rec_name = 'nombre'
    nombre = fields.Char('Actividad de mano de obra', required=True)

class mano_obra_video(models.Model):
    _name = 'mano.video'
    _rec_name = 'nombre'
    nombre = fields.Char('Actividad de mano de obra', required=True)

class mano_obra_acceso(models.Model):
    _name = 'mano.acceso'
    _rec_name = 'nombre'
    nombre = fields.Char('Actividad de mano de obra', required=True)

class video_mano(models.Model):
    _name = 'video.mano'
    _rec_name = 'nombre'
    nombre = fields.Many2one('materiales.video', required=True)
    observacion = fields.Many2many('mano.video', string='Mano de obra')
    zona = fields.Char('¿PERTENECE A UNA ZONA O UBICACIÓN EN ESPECIAL SOBRE LA UCP?')
    cobertura = fields.Char('¿CUBRE UN ÁREA ESPECÍFICA?')
    placa = fields.Char('Placa')
    img = fields.Binary('Soporte visual')
    segunda_placa = fields.Char('Serial del elemento desmontado')
    img2 = fields.Binary('Soporte visual')
    opuesto = fields.Many2one('acta.servicio', string="", readonly="True")

class materiales_video(models.Model):
    _name = 'materiales.video'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre del equipo', required=True)

class control_acceso(models.Model):
    _name = 'control.acceso'
    _rec_name = 'nombre'
    nombre = fields.Many2one('materiales.control', required=True)
    observacion = fields.Many2many('mano.acceso', string='Mano de obra')
    zona = fields.Char('¿PERTENECE A UNA ZONA O UBICACIÓN EN ESPECIAL SOBRE LA UCP?')
    cobertura = fields.Char('¿CUBRE UN ÁREA ESPECÍFICA?')
    placa = fields.Char('Placa')
    img = fields.Binary('Soporte visual')
    segunda_placa = fields.Char('Serial del elemento desmontado')
    img2 = fields.Binary('Soporte visual')
    opuesto = fields.Many2one('acta.servicio', string="", readonly="True")

class materiales_control(models.Model):
    _name = 'materiales.control'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre del equipo', required=True)

class equipo_liviado(models.Model):
    _name = 'equipo.liviano'
    _rec_name = 'nombre'
    #la informacion del nombre quedo cruzada
    nombre = fields.Many2one('material.equipo.liviano', required=True, string='Selecciones el elemento sobre el que trabajo')
    observacion = fields.Many2many('observacion.equipo.liviano', string='Mano de obra')
    compartimiento = fields.Many2many('compartimiento.equipo.liviano',string='Seleccione el compartimiento sobre el que trabajó')
    placa = fields.Char('Placa')
    img = fields.Binary('Soporte visual')
    segunda_placa = fields.Char('Serial del elemento desmontado')
    img2 = fields.Binary('Soporte visual')
    opuesto = fields.Many2one('acta.servicio', string="", readonly="True")

class material_equipo_liviano(models.Model):
    _name = 'material.equipo.liviano'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre del equipo', required=True)

class observacion_equipo_liviano(models.Model):
    _name = 'observacion.equipo.liviano'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre de la mano de obra', required=True)

class compartimiento_equipo_liviano(models.Model):
    _name = 'compartimiento.equipo.liviano'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre del compartimiento', required=True)

class equipo_pesado(models.Model):
    _name = 'equipo.pesado'
    _rec_name = 'nombre'
    nombre = fields.Many2one('material.equipo.pesado', required=True, string='Selecciones el elemento sobre el que trabajo')
    observacion = fields.Many2many('observacion.equipo.pesado', string='Mano de obra')
    compartimiento = fields.Many2many('compartimiento.equipo.pesado',string='Seleccione el compartimiento sobre el que trabajó')
    placa = fields.Char('Placa')
    img = fields.Binary('Soporte visual')
    segunda_placa = fields.Char('Serial del elemento desmontado')
    img2 = fields.Binary('Soporte visual')
    opuesto = fields.Many2one('acta.servicio', string="", readonly="True")

class material_equipo_pesado(models.Model):
    _name = 'material.equipo.pesado'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre del equipo', required=True)

class observacion_equipo_pesado(models.Model):
    _name = 'observacion.equipo.pesado'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre de la mano de obra', required=True)

class compartimiento_equipo_pesado(models.Model):
    _name = 'compartimiento.equipo.pesado'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre del compartimiento', required=True)

class suministros_metalmecanicos(models.Model):
    _name = 'suministros_metalmecanicos'
    _rec_name = 'lista_cliente'
    lista_cliente = fields.Many2one('suministro.metalmecanicos',
                                    string='Si suministró algo, favor seleccionarlo de la siguiente lista:')
    cantidad = fields.Integer('cantidad', size=2, default=1)
    elementocambiado = fields.Selection([('r1', 'ENTREGADO'),
                                         ('r2', 'CAMBIADO')], string='EL ELEMENTO FUE:')
    # en caso dado que sea cambiado
    propiedad_material = fields.Selection([('r1', 'El cliente'),
                                           ('r2', 'El proveedor')
                                           ], string='El elemento cambiado es propiedad de:')
    indicaciones_material = fields.Selection([('r1', 'Nuevo'),
                                              ('r2', 'Usado')
                                              ], string='El elemento es:')
    opuesto = fields.Many2one('acta.servicio', string="", readonly="True")

    serial = fields.Char(string='ingrese el serial si lo posee')

class suministro_metalmecanicos(models.Model):
    _name = 'suministro.metalmecanicos'
    _rec_name = 'nombre'
    nombre = fields.Char('Nombre del compartimiento', required=True)