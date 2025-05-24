package com.presca.modul4.viewmodel

import android.util.Log
import androidx.lifecycle.ViewModel
import com.presca.modul4.data.twiceMusicList
import com.presca.modul4.models.Music
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow

class MusicViewModel : ViewModel() {
    private val _musicList = MutableStateFlow(twiceMusicList)
    val musicList: StateFlow<List<Music>> = _musicList

    fun logSelect(music: Music) {
        Log.d("MusicViewModel", "Musik: ${music.title}")
    }

    fun logDetailClick() {
        Log.d("MusicViewModel", "Tombol detail ditekan")
    }

    fun logExternalClick(url: String) {
        Log.d("MusicViewModel", "link website informasi musik ditekan: $url")
    }

    init {
        Log.d("MusicViewModel", "Musik list berisi ${_musicList.value.size} items")
    }
}