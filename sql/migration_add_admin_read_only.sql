-- Migración: agregar valor 'admin_read_only' al enum rol_enum
-- Ejecutar en Supabase SQL Editor si la BD fue creada antes de esta funcionalidad.
ALTER TYPE rol_enum ADD VALUE IF NOT EXISTS 'admin_read_only';
