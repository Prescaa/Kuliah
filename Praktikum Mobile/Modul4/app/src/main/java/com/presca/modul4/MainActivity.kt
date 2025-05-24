package com.presca.modul4

import android.content.Intent
import android.net.Uri
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.activity.viewModels
import androidx.compose.runtime.Composable
import androidx.compose.ui.platform.LocalContext
import androidx.navigation.NavHostController
import androidx.navigation.compose.NavHost
import androidx.navigation.compose.composable
import androidx.navigation.compose.rememberNavController
import com.presca.modul4.ui.screens.MusicDetailScreen
import com.presca.modul4.ui.screens.MusicListScreen
import com.presca.modul4.ui.theme.Modul4Theme
import com.presca.modul4.viewmodel.MusicViewModel
import com.presca.modul4.viewmodel.MusicViewModelFactory

class MainActivity : ComponentActivity() {
    private val viewModel: MusicViewModel by viewModels { MusicViewModelFactory() }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        setContent {
            Modul4Theme {
                val navController = rememberNavController()
                AppNavigation(navController, viewModel)
            }
        }
    }
}

@Composable
fun AppNavigation(navController: NavHostController, viewModel: MusicViewModel) {
    val context = LocalContext.current
    NavHost(navController, startDestination = "music_list") {
        composable("music_list") {
            MusicListScreen(
                viewModel = viewModel,
                onMusicClick = {
                    viewModel.logDetailClick()
                    viewModel.logSelect(it)
                    navController.navigate("detail/${it.id}")
                },
                onExternalClick = {
                    viewModel.logExternalClick(it)
                    context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(it)))
                }
            )
        }
        composable("detail/{musicId}") { backStackEntry ->
            val musicId = backStackEntry.arguments?.getString("musicId")?.toIntOrNull()
            val music = viewModel.musicList.value.find { it.id == musicId }
            music?.let {
                MusicDetailScreen(it, navController)
            }
        }
    }
}