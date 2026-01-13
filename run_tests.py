#!/usr/bin/env python3
"""
Script para ejecutar Unit Tests automáticamente
Genera un reporte detallado de los resultados
"""

import unittest
import sys
from io import StringIO
from datetime import datetime
import os

def run_tests():
    """
    Ejecuta todos los unit tests y genera un reporte
    """
    print("=" * 70)
    print("🧪 EJECUTANDO UNIT TESTS - PET SHOP API")
    print("=" * 70)
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    print()
    
    
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    
    runner = unittest.TextTestRunner(verbosity=2)
    

    print("Ejecutando tests...\n")
    result = runner.run(suite)
    

    print("\n")
    print("=" * 70)
    print("📊 REPORTE DE RESULTADOS")
    print("=" * 70)
    
    total_tests = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    skipped = len(result.skipped)
    success = total_tests - failures - errors - skipped
    
    print(f"\n✅ Tests exitosos: {success}/{total_tests}")
    print(f"❌ Tests fallidos: {failures}/{total_tests}")
    print(f"⚠️  Errores: {errors}/{total_tests}")
    print(f"⏭️  Omitidos: {skipped}/{total_tests}")
    
    
    if total_tests > 0:
        success_rate = (success / total_tests) * 100
        print(f"\n📈 Tasa de éxito: {success_rate:.2f}%")
    
    
    if failures > 0:
        print("\n" + "=" * 70)
        print("❌ DETALLES DE TESTS FALLIDOS")
        print("=" * 70)
        for test, traceback in result.failures:
            print(f"\nTest: {test}")
            print(f"Error:\n{traceback}")
    
    
    if errors > 0:
        print("\n" + "=" * 70)
        print("⚠️  DETALLES DE ERRORES")
        print("=" * 70)
        for test, traceback in result.errors:
            print(f"\nTest: {test}")
            print(f"Error:\n{traceback}")
    
    print("\n" + "=" * 70)
    
    
    save_report(result, total_tests, success, failures, errors, skipped)
    
    
    if result.wasSuccessful():
        print("✅ TODOS LOS TESTS PASARON EXITOSAMENTE")
        print("=" * 70)
        return 0
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("=" * 70)
        return 1

def save_report(result, total, success, failures, errors, skipped):
    """
    Guarda el reporte de tests en un archivo
    """
    report_file = f"test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("=" * 70 + "\n")
        f.write("REPORTE DE UNIT TESTS - PET SHOP API\n")
        f.write("=" * 70 + "\n")
        f.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 70 + "\n\n")
        
        f.write("RESUMEN DE RESULTADOS:\n")
        f.write(f"  Total de tests ejecutados: {total}\n")
        f.write(f"  Tests exitosos: {success}\n")
        f.write(f"  Tests fallidos: {failures}\n")
        f.write(f"  Errores: {errors}\n")
        f.write(f"  Omitidos: {skipped}\n")
        
        if total > 0:
            success_rate = (success / total) * 100
            f.write(f"  Tasa de éxito: {success_rate:.2f}%\n")
        
        if failures > 0:
            f.write("\n" + "=" * 70 + "\n")
            f.write("TESTS FALLIDOS:\n")
            f.write("=" * 70 + "\n")
            for test, traceback in result.failures:
                f.write(f"\nTest: {test}\n")
                f.write(f"Error:\n{traceback}\n")
        
        if errors > 0:
            f.write("\n" + "=" * 70 + "\n")
            f.write("ERRORES:\n")
            f.write("=" * 70 + "\n")
            for test, traceback in result.errors:
                f.write(f"\nTest: {test}\n")
                f.write(f"Error:\n{traceback}\n")
        
        f.write("\n" + "=" * 70 + "\n")
        if result.wasSuccessful():
            f.write("RESULTADO: TODOS LOS TESTS PASARON ✅\n")
        else:
            f.write("RESULTADO: ALGUNOS TESTS FALLARON ❌\n")
        f.write("=" * 70 + "\n")
    
    print(f"\n📄 Reporte guardado en: {report_file}")

if __name__ == '__main__':
    sys.exit(run_tests())