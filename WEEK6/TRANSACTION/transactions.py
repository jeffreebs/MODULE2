

from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models_transactions import Product, User, Invoice, InvoiceStatus, engine
from datetime import datetime


Session = sessionmaker(bind=engine)


class TransactionError(Exception):
    """Custom exception for transaction errors"""
    pass


def create_purchase_transaction(user_id, product_id, quantity):
    session = Session()
    
    try:
        print("\n" + "="*60)
        print("🛒 INICIANDO TRANSACCIÓN DE COMPRA")
        print("="*60)
        
        
        print(f"\n1️⃣ Validando que el usuario existe...")
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise TransactionError(f"❌ Usuario con id {user_id} no existe")
        print(f"   ✅ Usuario encontrado: {user.name}")
        
        
        print(f"\n2️⃣ Validando stock del producto...")
        product = session.query(Product).filter_by(id=product_id).first()
        if not product:
            raise TransactionError(f"❌ Producto con id {product_id} no existe")
        
        if product.stock < quantity:
            raise TransactionError(
                f"❌ Stock insuficiente. Disponible: {product.stock}, Solicitado: {quantity}"
            )
        print(f"   ✅ Producto: {product.name}")
        print(f"   ✅ Stock disponible: {product.stock}")
        print(f"   ✅ Cantidad solicitada: {quantity}")
        
        
        print(f"\n3️⃣ Creando factura...")
        total = product.price * quantity
        
        new_invoice = Invoice(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total=total,
            status=InvoiceStatus.COMPLETED,
            date=datetime.now()
        )
        session.add(new_invoice)
        print(f"   ✅ Factura creada")
        print(f"   💰 Total: ${total:.2f}")
        
        
        print(f"\n4️⃣ Actualizando stock...")
        old_stock = product.stock
        product.stock -= quantity
        print(f"   ✅ Stock actualizado: {old_stock} → {product.stock}")
        
        session.commit()
        
        print("\n" + "="*60)
        print("✅ TRANSACCIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print(f"📄 Factura ID: {new_invoice.id}")
        print(f"👤 Usuario: {user.name}")
        print(f"📦 Producto: {product.name}")
        print(f"🔢 Cantidad: {quantity}")
        print(f"💰 Total: ${total:.2f}")
        print(f"📊 Nuevo stock: {product.stock}")
        
        return new_invoice
        
    except TransactionError as e:
        
        session.rollback()
        print("\n" + "="*60)
        print("❌ TRANSACCIÓN FALLIDA - ROLLBACK EJECUTADO")
        print("="*60)
        print(f"Error: {str(e)}")
        print("Todos los cambios han sido revertidos.")
        return None
        
    except SQLAlchemyError as e:
        session.rollback()
        print("\n" + "="*60)
        print("❌ ERROR DE BASE DE DATOS - ROLLBACK EJECUTADO")
        print("="*60)
        print(f"Error: {str(e)}")
        return None
        
    finally:
        session.close()


def create_return_transaction(invoice_id):
    session = Session()
    
    try:
        print("\n" + "="*60)
        print("↩️  INICIANDO TRANSACCIÓN DE RETORNO")
        print("="*60)
        
        
        print(f"\n1️⃣ Validando que la factura existe...")
        invoice = session.query(Invoice).filter_by(id=invoice_id).first()
        if not invoice:
            raise TransactionError(f"❌ Factura con id {invoice_id} no existe")
        
        if invoice.status == InvoiceStatus.RETURNED:
            raise TransactionError(f"❌ Esta factura ya fue retornada anteriormente")
        
        print(f"   ✅ Factura encontrada: ID {invoice.id}")
        print(f"   📦 Producto ID: {invoice.product_id}")
        print(f"   🔢 Cantidad: {invoice.quantity}")
        print(f"   📊 Estado actual: {invoice.status.value}")
        
        
        print(f"\n2️⃣ Restaurando stock del producto...")
        product = session.query(Product).filter_by(id=invoice.product_id).first()
        if not product:
            raise TransactionError(f"❌ Producto asociado no existe")
        
        old_stock = product.stock
        product.stock += invoice.quantity
        print(f"   ✅ Stock restaurado: {old_stock} → {product.stock}")
        
        
        print(f"\n3️⃣ Actualizando factura...")
        invoice.status = InvoiceStatus.RETURNED
        print(f"   ✅ Factura marcada como: {invoice.status.value}")
        
        
        session.commit()
        
        print("\n" + "="*60)
        print("✅ RETORNO COMPLETADO EXITOSAMENTE")
        print("="*60)
        print(f"📄 Factura ID: {invoice.id}")
        print(f"📦 Producto: {product.name}")
        print(f"🔢 Cantidad retornada: {invoice.quantity}")
        print(f"📊 Nuevo stock: {product.stock}")
        print(f"💰 Monto devuelto: ${invoice.total:.2f}")
        
        return invoice
        
    except TransactionError as e:
        
        session.rollback()
        print("\n" + "="*60)
        print("❌ RETORNO FALLIDO - ROLLBACK EJECUTADO")
        print("="*60)
        print(f"Error: {str(e)}")
        print("Todos los cambios han sido revertidos.")
        return None
        
    except SQLAlchemyError as e:
        session.rollback()
        print("\n" + "="*60)
        print("❌ ERROR DE BASE DE DATOS - ROLLBACK EJECUTADO")
        print("="*60)
        print(f"Error: {str(e)}")
        return None
        
    finally:
        session.close()


def view_all_invoices():
    """Helper function to view all invoices"""
    session = Session()
    try:
        invoices = session.query(Invoice).all()
        print("\n" + "="*60)
        print(f"📋 TODAS LAS FACTURAS ({len(invoices)})")
        print("="*60)
        for inv in invoices:
            print(f"  {inv}")
        return invoices
    finally:
        session.close()


def view_all_products():
    """Helper function to view all products"""
    session = Session()
    try:
        products = session.query(Product).all()
        print("\n" + "="*60)
        print(f"📦 TODOS LOS PRODUCTOS ({len(products)})")
        print("="*60)
        for prod in products:
            print(f"  {prod}")
        return products
    finally:
        session.close()


def view_all_users():
    """Helper function to view all users"""
    session = Session()
    try:
        users = session.query(User).all()
        print("\n" + "="*60)
        print(f"👥 TODOS LOS USUARIOS ({len(users)})")
        print("="*60)
        for user in users:
            print(f"  {user}")
        return users
    finally:
        session.close()


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🧪 TESTING TRANSACTION OPERATIONS")
    print("="*70)
    
    
    
    
    
    view_all_users()
    view_all_products()
    
    
    print("\n\n" + "🔹"*35)
    print("TEST 1: COMPRA EXITOSA")
    print("🔹"*35)
    invoice1 = create_purchase_transaction(user_id=1, product_id=1, quantity=2)
    
    
    view_all_products()
    view_all_invoices()
    
    
    print("\n\n" + "🔹"*35)
    print("TEST 2: COMPRA FALLIDA (Stock insuficiente)")
    print("🔹"*35)
    invoice2 = create_purchase_transaction(user_id=1, product_id=1, quantity=100)
    
    
    view_all_products()
    
    
    if invoice1:
        print("\n\n" + "🔹"*35)
        print("TEST 3: RETORNO EXITOSO")
        print("🔹"*35)
        create_return_transaction(invoice_id=invoice1.id)
        
    
        view_all_products()
        view_all_invoices()
    
    
    print("\n\n" + "🔹"*35)
    print("TEST 4: RETORNO FALLIDO (Factura no existe)")
    print("🔹"*35)
    create_return_transaction(invoice_id=9999)
    
    print("\n✅ All tests completed!")