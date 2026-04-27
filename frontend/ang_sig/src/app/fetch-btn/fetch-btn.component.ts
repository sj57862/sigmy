import { Component } from '@angular/core';
import { environment } from '../../environments/environment';

@Component({
  selector: 'app-fetch-btn',
  standalone: true,
  imports: [],
  templateUrl: './fetch-btn.component.html',
  styleUrl: './fetch-btn.component.css'
})
export class FetchBtnComponent {
  async onClick(){
    try{
      let data = await fetch(`${environment.API_URL}/`);
      let j_data = await data.json();
      console.log(j_data);
    }catch(e){
      console.log('jakis blad :0');
    }
  }
}
