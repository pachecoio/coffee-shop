import { HttpClient, HttpHandler } from "@angular/common/http";
import { CUSTOM_ELEMENTS_SCHEMA } from "@angular/core";
import { async, ComponentFixture, TestBed } from "@angular/core/testing";
import { AngularDelegate, ModalController } from "@ionic/angular";

import { DrinkFormComponent } from "./drink-form.component";

describe("DrinkFormComponent", () => {
  let component: DrinkFormComponent;
  let fixture: ComponentFixture<DrinkFormComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [DrinkFormComponent],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [ModalController, AngularDelegate, HttpClient, HttpHandler],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DrinkFormComponent);
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
