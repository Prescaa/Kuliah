<?php namespace App\Database\Migrations;

use CodeIgniter\Database\Migration;

class CreateBuku extends Migration
{
    public function up()
    {
        $this->forge->addField([
            'id' => [
                'type' => 'BIGINT',
                'constraint' => 20,
                'unsigned' => true,
                'auto_increment' => true
            ],
            'judul' => [
                'type' => 'VARCHAR',
                'constraint' => 255,
                'null' => false
            ],
            'penulis' => [
                'type' => 'VARCHAR',
                'constraint' => 100,
                'null' => false
            ],
            'penerbit' => [
                'type' => 'VARCHAR',
                'constraint' => 100,
                'null' => false
            ],
            'tahun_terbit' => [
                'type' => 'YEAR',
                'null' => false
            ]
        ]);
        $this->forge->addKey('id', true);
        $this->forge->createTable('buku');
    }

    public function down()
    {
        $this->forge->dropTable('buku');
    }
}