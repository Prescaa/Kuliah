package com.presca.modul2

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.selection.selectable
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.text.KeyboardOptions
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.input.KeyboardType
import androidx.compose.ui.text.style.TextAlign
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import com.presca.modul2.ui.theme.Modul2Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Modul2Theme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = MaterialTheme.colorScheme.background
                ) {
                    TipCalculatorScreen()
                }
            }
        }
    }
}

@Composable
fun TipCalculatorScreen() {
    var costInput by rememberSaveable { mutableStateOf("") }
    var selectedOption by rememberSaveable { mutableStateOf(20) }
    var roundUp by rememberSaveable { mutableStateOf(false) }
    var tipResult by rememberSaveable { mutableStateOf("Tip Amount") }

    val context = LocalContext.current

    fun calculateTip() {
        val cost = costInput.toDoubleOrNull()

        if (cost == null || cost <= 0) {
            Toast.makeText(
                context,
                "Masukkan angka positif dan bukan nol!",
                Toast.LENGTH_SHORT
            ).show()
            return
        }

        val tip = TipCalculator.calculateTip(
            cost = cost,
            percentage = selectedOption,
            roundUp = roundUp
        )
        tipResult = "Tip Amount: \$${"%.2f".format(tip)}"
    }

    Column(
        modifier = Modifier
            .verticalScroll(rememberScrollState())
            .fillMaxWidth()
    ) {

        Box(
            modifier = Modifier
                .fillMaxWidth()
                .background(Color(0xFF6200EE))
                .padding(16.dp)
        ) {
            Text(
                text = "Tip Time",
                color = Color.White,
                fontSize = 20.sp,
                modifier = Modifier.align(Alignment.CenterStart)
            )
        }

        Column(
            modifier = Modifier
                .padding(16.dp)
                .fillMaxWidth(),
            verticalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            OutlinedTextField(
                value = costInput,
                onValueChange = { costInput = it },
                label = { Text("Cost of Service") },
                modifier = Modifier.fillMaxWidth(),
                keyboardOptions = KeyboardOptions(keyboardType = KeyboardType.Number),
                shape = RoundedCornerShape(8.dp),
                colors = TextFieldDefaults.colors(
                    focusedIndicatorColor = Color(0xFF6200EE),
                    unfocusedIndicatorColor = Color.Gray,
                    focusedContainerColor = Color.White,
                    unfocusedContainerColor = Color.White,
                    focusedLabelColor = Color(0xFF6200EE),
                    unfocusedLabelColor = Color.Gray
                ),
                singleLine = true
            )

            Text(
                text = "How was the service?",
                color = Color.Gray
            )

            val options = listOf(
                "Amazing (20%)" to 20,
                "Good (18%)" to 18,
                "Okay (15%)" to 15
            )

            options.forEach { (label, value) ->
                Row(
                    verticalAlignment = Alignment.CenterVertically,
                    modifier = Modifier
                        .fillMaxWidth()
                        .selectable(
                            selected = (selectedOption == value),
                            onClick = { selectedOption = value }
                        )
                        .padding(4.dp)
                ) {
                    RadioButton(
                        selected = (selectedOption == value),
                        onClick = { selectedOption = value }
                    )
                    Text(text = label)
                }
            }

            Row(
                verticalAlignment = Alignment.CenterVertically
            ) {
                Text("Round up tip?")
                Spacer(modifier = Modifier.weight(1f))
                Switch(
                    checked = roundUp,
                    onCheckedChange = { roundUp = it }
                )
            }

            Button(
                onClick = { calculateTip() },
                modifier = Modifier
                    .fillMaxWidth()
                    .height(48.dp),
                colors = ButtonDefaults.buttonColors(
                    containerColor = Color(0xFF6200EE)
                ),
                shape = RoundedCornerShape(0.dp)
            ) {
                Text("CALCULATE", color = Color.White, fontSize = 16.sp)
            }

            Text(
                text = tipResult,
                modifier = Modifier
                    .fillMaxWidth()
                    .padding(top = 4.dp),
                textAlign = TextAlign.End,
                color = Color.Gray
            )
        }
    }
}
