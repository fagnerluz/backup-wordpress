#!/usr/bin/python3
import os
import re
import time

# VARIAVEIS
bucket = ""
www_dir = ""
wordpress_dirs = ['wp-content/themes', 'wp-content/plugins', 'wp-content/uploads']
wordpress_files = ['wp-config.php', '.htaccess']
timestamp = time.strftime('%Y-%m-%d')

def sync_wordpress_dir():
    os.system('aws s3 sync ' + www_dir + diretorio + '/' + wordpress_dir + ' '  + bucket + '/' + diretorio + '/' + wordpress_dir + '/')

def sync_wordpress_file():
    os.system('aws s3 cp ' + www_dir + diretorio + '/' + wordpress_file + ' '  + bucket + '/' + diretorio + '/')

def busca_info_wp_config(info):
    with open(wp_config, "r") as f:
        data = f.readlines()
        for line in data:
            if line.__contains__(info):
                values = re.findall(r',.*\)', line)
                for k in values:
                    value = "".join(re.findall("[a-zA-Z\.]+", k))
                    return (value)

def dump_mysql(db_user,db_pass,db_host,db_name):
    os.popen("mysqldump -u %s -p%s -h %s %s > /tmp/%s.sql" % (db_user,db_pass,db_host,db_name,db_name))

lista_diretorios = [ name for name in os.listdir(www_dir) if os.path.isdir(os.path.join(str(www_dir), name))]
for diretorio in lista_diretorios:
    sub_diretorio = [ name for name in os.listdir(www_dir + diretorio) if os.path.isdir(os.path.join(str(www_dir + diretorio), name))]
    for sub_diretorio in sub_diretorio:
        if 'wp-content' in sub_diretorio:
            for wordpress_dir in wordpress_dirs:
                sync_wordpress_dir()
            for wordpress_file in wordpress_files:
                sync_wordpress_file()

            wp_config = www_dir + diretorio + '/wp-config.php'
            db_infos = ['DB_NAME', 'DB_USER', 'DB_PASSWORD', 'DB_HOST']

            for db_info in db_infos:
                if db_info == 'DB_NAME':
                    db_name = busca_info_wp_config(db_info)
                if db_info == 'DB_USER':
                    db_user = busca_info_wp_config(db_info)
                if db_info == 'DB_PASSWORD':
                    db_pass = busca_info_wp_config(db_info)
                if db_info == 'DB_HOST':
                    db_host = busca_info_wp_config(db_info)

            dump_mysql(db_user,db_pass,db_host,db_name)
