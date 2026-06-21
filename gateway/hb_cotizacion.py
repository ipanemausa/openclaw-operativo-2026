import os
import requests
from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, Cotizacion

hb_bp = Blueprint('hb_jewelry', __name__)

MARKETING_URL = os.getenv('MARKETING_URL', 'http://openclaw_marketing_generator:5000')
SHOPIFY_URL = os.getenv('SHOPIFY_URL', 'http://openclaw_shopify_integration:5000')

def crear_tabla_cotizaciones():
    pass

@hb_bp.route('/api/flows/cotizacion', methods=['POST'])
def hb_cotizacion():
    data = request.get_json(silent=True) or {}
    faltantes = [c for c in ['nombre','email','tipo_pieza','descripcion','presupuesto'] if not data.get(c)]
    if faltantes:
        return jsonify({'status': 'error', 'campos_faltantes': faltantes}), 400

    nombre = data['nombre']
    email = data['email']
    tipo_pieza = data['tipo_pieza']
    presupuesto = data['presupuesto']
    descripcion = data['descripcion']

    # ESTADO 1: Guardar en BD
    try:
        coti = Cotizacion(
            cliente_nombre=nombre,
            cliente_email=email,
            tipo_pieza=tipo_pieza,
            material=data.get('material', ''),
            ocasion=data.get('ocasion', ''),
            presupuesto=presupuesto,
            descripcion=descripcion,
            referencias=data.get('referencias', ''),
            estado='recibida'
        )
        db.session.add(coti)
        db.session.commit()
        cid = coti.id
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'mensaje': 'BD: ' + str(e)}), 500

    # ESTADO 2: Llamar agente marketing
    propuesta = ''
    try:
        res = requests.post(
            MARKETING_URL + '/generate',
            json={'nombre': nombre, 'tipo_pieza': tipo_pieza, 'presupuesto': presupuesto, 'descripcion': descripcion},
            timeout=30
        )
        mdata = res.json()
        propuesta = mdata.get('propuesta', '')
        if propuesta:
            c = Cotizacion.query.get(cid)
            if c:
                c.propuesta = propuesta
                c.estado = 'propuesta_generada'
                db.session.commit()
    except Exception as e:
        db.session.rollback()
        print('[HB] marketing error: ' + str(e))

    # ESTADO 3: Llamar agente shopify
    shopify_result = {}
    try:
        res2 = requests.post(
            SHOPIFY_URL + '/sync',
            json={'cotizacion_id': cid, 'tipo_pieza': tipo_pieza, 'presupuesto': presupuesto, 'cliente': nombre},
            timeout=15
        )
        shopify_result = res2.json()
    except Exception as e:
        print('[HB] shopify error: ' + str(e))

    return jsonify({
        'status': 'ok',
        'cotizacion_id': cid,
        'propuesta': propuesta,
        'shopify': shopify_result,
        'mensaje': 'Flujo completo ejecutado'
    }), 200

@hb_bp.route('/api/flows/cotizacion/<int:cid>', methods=['GET'])
def hb_get_cotizacion(cid):
    try:
        row = Cotizacion.query.get(cid)
        if not row:
            return jsonify({'status': 'error', 'mensaje': 'No encontrada'}), 404
        d = {
            "id": row.id,
            "cliente_nombre": row.cliente_nombre,
            "cliente_email": row.cliente_email,
            "tipo_pieza": row.tipo_pieza,
            "material": row.material,
            "ocasion": row.ocasion,
            "presupuesto": row.presupuesto,
            "descripcion": row.descripcion,
            "referencias": row.referencias,
            "clasificacion": row.clasificacion,
            "propuesta": row.propuesta,
            "estado": row.estado,
            "created_at": row.created_at.isoformat() if row.created_at else None,
            "updated_at": row.updated_at.isoformat() if row.updated_at else None
        }
        return jsonify({'status': 'ok', 'cotizacion': d}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

@hb_bp.route('/hb/dashboard', methods=['GET'])
def hb_dashboard():
    try:
        total = Cotizacion.query.count()
        rows = Cotizacion.query.order_by(Cotizacion.created_at.desc()).limit(20).all()
        data_rows = [{
            "id": r.id,
            "cliente_nombre": r.cliente_nombre,
            "tipo_pieza": r.tipo_pieza,
            "estado": r.estado,
            "created_at": r.created_at.isoformat() if r.created_at else None
        } for r in rows]
        
        return jsonify({'status': 'ok', 'stats': {"total": total}, 'cotizaciones': data_rows}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500

@hb_bp.route('/api/flows/cotizacion/<int:cid>/estado', methods=['PATCH'])
def hb_update_estado(cid):
    data = request.get_json(silent=True) or {}
    estado = data.get('estado', '').strip()
    validos = ['recibida','propuesta_generada','aprobada','en_produccion','entregada','cancelada']
    if estado not in validos:
        return jsonify({'status': 'error', 'mensaje': 'Estado invalido', 'validos': validos}), 400
    try:
        row = Cotizacion.query.get(cid)
        if not row:
            return jsonify({'status': 'error', 'mensaje': 'No encontrada'}), 404
        row.estado = estado
        db.session.commit()
        return jsonify({'status': 'ok', 'id': cid, 'nuevo_estado': estado}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'mensaje': str(e)}), 500
