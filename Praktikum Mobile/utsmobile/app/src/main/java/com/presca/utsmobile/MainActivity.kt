package com.presca.utsmobile

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp

class MainActivity : ComponentActivity() {

    private val mahasiswa = Mahasiswa()

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Surface(modifier = Modifier.fillMaxSize()) {
                var currentPage by rememberSaveable { mutableStateOf("home") }

                when (currentPage) {
                    "home" -> HalamanUtama(mahasiswa) {
                        currentPage = "detail"
                    }
                    "detail" -> HalamanDetail(mahasiswa) {
                        currentPage = "home"
                    }
                }
            }
        }
    }
}

@Composable
fun HalamanUtama(mahasiswa: Mahasiswa, onClick: () -> Unit) {
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp),
        verticalArrangement = Arrangement.Top
    ) {
        Text(
            text = "Daftar Mahasiswa",
            fontSize = 20.sp,
            fontWeight = FontWeight.SemiBold,
            modifier = Modifier.padding(bottom = 16.dp)
        )

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(
                    color = Color(0xFFF5F5DC),
                    shape = RoundedCornerShape(8.dp)
                )
                .padding(16.dp)
        ) {
            Column {
                Text(
                    text = mahasiswa.nama,
                    fontSize = 18.sp,
                    fontWeight = FontWeight.Bold,
                    color = Color.Black
                )
                Text(
                    text = "Prodi: ${mahasiswa.jurusan}",
                    fontSize = 14.sp,
                    color = Color.DarkGray
                )
                Text(
                    text = "NIM: ${mahasiswa.nim}",
                    fontSize = 14.sp,
                    color = Color.DarkGray
                )
                Text(
                    text = "IPK: ${mahasiswa.ipk}",
                    fontSize = 14.sp,
                    color = Color.DarkGray
                )

                Spacer(modifier = Modifier.height(12.dp))

                Button(
                    onClick = onClick,
                    shape = RoundedCornerShape(8.dp)
                ) {
                    Text("Lihat Detail")
                }
            }
        }
    }
}

@Composable
fun HalamanDetail(mahasiswa: Mahasiswa, onBack: () -> Unit) {
    val scrollState = rememberScrollState()

    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(24.dp)
            .verticalScroll(scrollState),
        horizontalAlignment = Alignment.CenterHorizontally
    ) {
        Image(
            painter = painterResource(id = mahasiswa.fotoRes),
            contentDescription = "Foto Mahasiswa",
            modifier = Modifier
                .size(180.dp)
                .padding(bottom = 16.dp),
            contentScale = ContentScale.Crop
        )

        Text(mahasiswa.nama, fontSize = 24.sp, fontWeight = FontWeight.Bold)
        Text("NIM: ${mahasiswa.nim}", fontSize = 16.sp)
        Text("Semester: ${mahasiswa.semester}", fontSize = 16.sp)
        Text("IPK: ${mahasiswa.ipk}", fontSize = 16.sp)

        Spacer(modifier = Modifier.height(16.dp))
        SectionHeader("Biografi")
        Text(
            text = mahasiswa.bio,
            fontSize = 14.sp,
            textAlign = TextAlign.Justify
        )

        Spacer(modifier = Modifier.height(16.dp))
        SectionHeader("Kontak")
        InfoText("Email: ${mahasiswa.email}")
        InfoText("No HP: ${mahasiswa.noHp}")

        Spacer(modifier = Modifier.height(32.dp))

        Button(onClick = onBack, shape = RoundedCornerShape(8.dp)) {
            Text("Kembali")
        }
    }
}

@Composable
fun SectionHeader(title: String) {
    Text(
        text = title,
        fontSize = 18.sp,
        fontWeight = FontWeight.SemiBold,
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 8.dp),
        color = Color(0xFF6200EA)
    )
}

@Composable
fun InfoText(text: String) {
    Text(
        text = text,
        fontSize = 14.sp,
        color = Color.DarkGray,
        modifier = Modifier
            .fillMaxWidth()
            .padding(vertical = 2.dp)
    )
}
