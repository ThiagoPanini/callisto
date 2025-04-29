/* --------------------------------------------------------
ARQUIVO: main.tf

Arquivo principal de definição de recursos deste projeto
Terraform.
-------------------------------------------------------- */

# Criando bucket S3 caos aplicável
resource "aws_s3_bucket" "files_bucket" {
  count         = var.flag_create_s3_bucket ? 1 : 0
  bucket        = local.s3_bucket_name
  force_destroy = true
}

# Realizando o upload de objetos pro S3
resource "aws_s3_object" "files" {
  for_each = local.tables_map
  bucket   = local.s3_bucket_name
  key      = "${each.value.schema.database_name}/${each.value.schema.table_name}/${each.key}"
  source   = each.value.file_path

  depends_on = [
    aws_s3_bucket.files_bucket
  ]
}

# Criando databases no Glue Data Catalog
resource "aws_glue_catalog_database" "databases" {
  for_each     = toset([for table_map in local.tables_map : table_map.schema.database_name])
  name         = each.value
  location_uri = "${local.s3_bucket_name}/${each.value}/"

  depends_on = [
    aws_s3_object.files
  ]
}

# Criando tabelas no Glue Data Catalog
resource "aws_glue_catalog_table" "tables" {
  for_each      = local.tables_map
  database_name = each.value.schema.database_name
  name          = each.value.schema.table_name
  description   = each.value.schema.table_description

  table_type = "EXTERNAL_TABLE"

  parameters = {
    "EXTERNAL"       = "TRUE"
    "classification" = "csv"
  }

  storage_descriptor {
    location      = "s3://${local.s3_bucket_name}/${each.value.schema.database_name}/${each.value.schema.table_name}/"
    input_format  = "org.apache.hadoop.mapred.TextInputFormat"
    output_format = "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat"

    ser_de_info {
      name                  = "stream-${each.value.schema.table_name}"
      serialization_library = "org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe"

      parameters = {
        "skip.header.line.count" = "1"                   # Ignorar a primeira linha de cabeçalho
        "field.delim"            = ";"                   # Delimitador de campo (vírgula)
        "timestamp.formats"      = "yyyy-MM-dd HH:mm:ss" # Formato de timestamp
      }
    }

    dynamic "columns" {
      for_each = each.value.schema.table_columns

      content {
        name    = columns.value.name
        type    = columns.value.type
        comment = columns.value.comment
      }
    }
  }

  depends_on = [
    aws_s3_object.files,
    aws_glue_catalog_database.databases
  ]
}
