package com.presca.modul3

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.presca.modul3.ui.theme.Modul3Theme

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            Modul3Theme {
                val navController = rememberNavController()
                AppNavigation(navController)
            }
        }
    }
}

@Composable
fun AppNavigation(navController: NavHostController) {
    val context = LocalContext.current

    NavHost(
        navController = navController,
        startDestination = "music_list"
    ) {
        composable("music_list") {
            MusicListScreen(
                onMusicClick = { music ->
                    navController.navigate("detail/${music.id}")
                },
                onExternalClick = { url ->
                    val intent = Intent(Intent.ACTION_VIEW, Uri.parse(url))
                    context.startActivity(intent)
                }
            )
        }

        composable("detail/{musicId}") { backStackEntry ->
            val musicId = backStackEntry.arguments?.getString("musicId")?.toIntOrNull()
            val music = musicList.find { it.id == musicId }
            music?.let {
                MusicDetailScreen(music = it, navController = navController)
            }
        }
    }
}
