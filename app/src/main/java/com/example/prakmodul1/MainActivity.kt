package com.example.prakmodul1

import android.os.Bundle
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.Image
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import com.example.prakmodul1.ui.theme.Prakmodul1Theme

class MainActivity : ComponentActivity() {
    companion object {
        private const val pesandouble = "Selamat anda dapat dadu double!"
        private const val kurangberuntung = "Anda belum beruntung!"
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            Prakmodul1Theme {
                DiceRollerApp()
            }
        }
    }

    @OptIn(ExperimentalMaterial3Api::class)
    @Composable
    fun DiceRollerApp() {
        var dice1 by rememberSaveable { mutableStateOf(0) }
        var dice2 by rememberSaveable { mutableStateOf(0) }

        val context = LocalContext.current

        Scaffold(
            topBar = {
                TopAppBar(
                    title = {
                        Text(
                            text = "Dice Roller",
                            style = MaterialTheme.typography.headlineMedium
                        )
                    },
                    colors = TopAppBarDefaults.topAppBarColors(
                        containerColor = Color(0xFF6200EE),
                        titleContentColor = Color.White
                    )
                )
            }
        ) { innerPadding ->
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .padding(innerPadding)
                    .padding(16.dp),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center
            ) {
                Row(
                    horizontalArrangement = Arrangement.spacedBy(32.dp),
                    verticalAlignment = Alignment.CenterVertically
                ) {
                    DiceImage(diceValue = dice1)
                    DiceImage(diceValue = dice2)
                }

                Spacer(modifier = Modifier.height(48.dp))

                Button(
                    onClick = {
                        dice1 = (1..6).random()
                        dice2 = (1..6).random()

                        val message = if (dice1 == dice2) pesandouble else kurangberuntung
                        Toast.makeText(context, message, Toast.LENGTH_SHORT).apply {
                            view?.setBackgroundResource(android.R.color.transparent)
                        }.show()
                    },
                    shape = RoundedCornerShape(0.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = Color(0xFF00BCD4),
                        contentColor = Color.White
                    ),
                    modifier = Modifier
                        .width(200.dp)
                        .height(50.dp)
                ) {
                    Text(
                        text = "ROLL DICE",
                        style = MaterialTheme.typography.labelLarge
                    )
                }
            }
        }
    }

    @Composable
    fun DiceImage(diceValue: Int) {
        val imageRes = when (diceValue) {
            0 -> R.drawable.dice_0
            1 -> R.drawable.dice_1
            2 -> R.drawable.dice_2
            3 -> R.drawable.dice_3
            4 -> R.drawable.dice_4
            5 -> R.drawable.dice_5
            else -> R.drawable.dice_6
        }

        Image(
            painter = painterResource(id = imageRes),
            contentDescription = "Dice showing $diceValue",
            modifier = Modifier.size(100.dp)
        )
    }
}
