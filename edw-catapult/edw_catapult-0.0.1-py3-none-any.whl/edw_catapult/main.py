import typer
import pyodbc as db
import time

def main(edw_name: str):
    sql = 'CREATE DATABASE ' + edw_name + ' COLLATE Latin1_General_CS_AS'
    connection_string = 'DSN=ETL;'
    conn = db.connect(connection_string, autocommit=True)
    csr = conn.cursor()

    try:
        typer.echo(f'Connecting to SQL Server database' + time.strftime(' %H:%M:%S'))
        typer.echo(f'Creating {edw_name} Database' + time.strftime(' %H:%M:%S'))
        csr.execute(sql)
        conn.commit()
    except Exception as e:
        typer.echo(e)
    finally:
        csr.close()
        conn.close()


if __name__ == "__main__":
    typer.run(main)