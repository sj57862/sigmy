import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FetchBtnComponent } from './fetch-btn.component';

describe('FetchBtnComponent', () => {
  let component: FetchBtnComponent;
  let fixture: ComponentFixture<FetchBtnComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FetchBtnComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FetchBtnComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
