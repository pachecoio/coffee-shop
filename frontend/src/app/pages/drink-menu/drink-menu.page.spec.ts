import { HttpClient, HttpHandler } from "@angular/common/http";
import { CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { async, ComponentFixture, TestBed } from "@angular/core/testing";
import { AngularDelegate, ModalController } from "@ionic/angular";
import { DrinksService } from 'src/app/services/drinks.service';

import { DrinkMenuPage } from "./drink-menu.page";

describe("DrinkMenuPage", () => {
  let component: DrinkMenuPage;
  let fixture: ComponentFixture<DrinkMenuPage>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DrinkMenuPage],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [ModalController, AngularDelegate, HttpClient, HttpHandler, DrinksService],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DrinkMenuPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  afterEach(() => {
    TestBed.resetTestingModule();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
