import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FetchBtnComponent } from './fetch-btn/fetch-btn.component';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet,FetchBtnComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'ang_sig';
}
