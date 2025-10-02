import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from './services/api.service';
import { State } from './models/state.model';
import { Obligation, ObligationsResponse } from './models/obligation.model';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  template: `
    <div class="container">
      <header class="header">
        <h1><i class="material-icons">calendar_today</i> Tax Calendar - Angular</h1>
        <p>Gerencie suas obrigações fiscais dos EUA</p>
      </header>

      <div [class]="'status-card ' + (connectionStatus === 'success' ? 'success' : 'error')">
        <div *ngIf="connectionStatus === 'loading'">
          <i class="material-icons">hourglass_empty</i> Conectando com o servidor...
        </div>
        <div *ngIf="connectionStatus === 'success'">
          <i class="material-icons">check_circle</i> {{ statusMessage }}
        </div>
        <div *ngIf="connectionStatus === 'error'">
          <i class="material-icons">error</i> {{ statusMessage }}
        </div>
      </div>

      <div class="card">
        <h2><i class="material-icons">filter_list</i> Filtros</h2>
        <div class="filters-grid">
          <div class="filter-group">
            <label for="stateSelect">Estado:</label>
            <select id="stateSelect" [(ngModel)]="selectedState" (change)="onStateChange()" class="form-control">
              <option value="">Selecione um estado</option>
              <option *ngFor="let state of states" [value]="state.code">{{ state.name }}</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label for="countySelect">Condado:</label>
            <select id="countySelect" [(ngModel)]="selectedCounty" (change)="onCountyChange()" 
                    [disabled]="!selectedState" class="form-control">
              <option value="">Selecione um condado</option>
              <option *ngFor="let county of counties" [value]="county.name">{{ county.name }}</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label for="citySelect">Cidade:</label>
            <select id="citySelect" [(ngModel)]="selectedCity" (change)="onCityChange()" 
                    [disabled]="!selectedCounty" class="form-control">
              <option value="">Selecione uma cidade</option>
              <option *ngFor="let city of cities" [value]="city.name">{{ city.name }}</option>
            </select>
          </div>
          
          <div class="filter-group">
            <label for="dateRange">Período:</label>
            <input type="month" id="dateRange" [(ngModel)]="selectedDateRange" 
                   (change)="onDateRangeChange()" class="form-control">
          </div>
        </div>
        
        <div class="filter-actions">
          <button (click)="clearFilters()" class="btn btn-secondary">
            <i class="material-icons">clear</i> Limpar Filtros
          </button>
          <button (click)="applyFilters()" class="btn btn-primary">
            <i class="material-icons">search</i> Aplicar Filtros
          </button>
        </div>
      </div>

      <div class="card">
        <h2><i class="material-icons">event_available</i> Obrigações</h2>
        <div *ngIf="loading" class="loading">
          <i class="material-icons">hourglass_empty</i> Carregando dados...
        </div>
        
        <div *ngIf="!loading && allObligations.length === 0" class="empty-state">
          <i class="material-icons">event_busy</i>
          <h3>Nenhuma obrigação encontrada</h3>
          <p>Ajuste os filtros para ver as obrigações fiscais</p>
        </div>
        
        <div *ngIf="!loading && allObligations.length > 0" class="obligations-list">
          <div *ngFor="let obligation of allObligations" 
               [class]="'obligation-card ' + obligation.jurisdiction_level">
            <div class="obligation-header">
              <h3 class="obligation-title">{{ obligation.name }}</h3>
              <span *ngIf="obligation.due_date" class="obligation-date">
                {{ formatDate(obligation.due_date) }}
              </span>
            </div>
            <p *ngIf="obligation.description" class="obligation-description">
              {{ obligation.description }}
            </p>
            <div class="obligation-meta">
              <span [class]="'obligation-level ' + obligation.jurisdiction_level">
                <i class="material-icons">{{ getLevelIcon(obligation.jurisdiction_level) }}</i>
                {{ getLevelName(obligation.jurisdiction_level) }}
              </span>
              <span *ngIf="obligation.category">
                <i class="material-icons">label</i> {{ obligation.category }}
              </span>
              <span *ngIf="obligation.frequency">
                <i class="material-icons">schedule</i> {{ obligation.frequency }}
              </span>
            </div>
          </div>
        </div>
      </div>

      <div class="card">
        <h2><i class="material-icons">bar_chart</i> Estatísticas</h2>
        <div class="stats-grid">
          <div class="stat-card federal">
            <div class="stat-icon">
              <i class="material-icons">flag</i>
            </div>
            <div class="stat-content">
              <h3>Federal</h3>
              <span class="stat-number">{{ obligations.federal.length }}</span>
            </div>
          </div>
          
          <div class="stat-card state">
            <div class="stat-icon">
              <i class="material-icons">place</i>
            </div>
            <div class="stat-content">
              <h3>Estadual</h3>
              <span class="stat-number">{{ obligations.state.length }}</span>
            </div>
          </div>
          
          <div class="stat-card county">
            <div class="stat-icon">
              <i class="material-icons">location_city</i>
            </div>
            <div class="stat-content">
              <h3>Condado</h3>
              <span class="stat-number">{{ obligations.county.length }}</span>
            </div>
          </div>
          
          <div class="stat-card municipality">
            <div class="stat-icon">
              <i class="material-icons">business</i>
            </div>
            <div class="stat-content">
              <h3>Municipal</h3>
              <span class="stat-number">{{ obligations.municipality.length }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .form-control {
      padding: 12px;
      border: 2px solid #e1e5e9;
      border-radius: 8px;
      font-size: 14px;
      transition: all 0.3s ease;
      width: 100%;
    }
    
    .form-control:focus {
      outline: none;
      border-color: #667eea;
      box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .form-control:disabled {
      background-color: #f8f9fa;
      color: #6c757d;
      cursor: not-allowed;
    }
  `]
})
export class AppComponent implements OnInit {
  title = 'Tax Calendar';
  
  // Status
  connectionStatus: 'loading' | 'success' | 'error' = 'loading';
  statusMessage = '';
  loading = false;
  
  // Dados
  states: State[] = [];
  counties: any[] = [];
  cities: any[] = [];
  obligations: ObligationsResponse = {
    federal: [],
    state: [],
    county: [],
    municipality: []
  };
  
  // Filtros
  selectedState = '';
  selectedCounty = '';
  selectedCity = '';
  selectedDateRange = '';
  
  // Obrigações combinadas
  allObligations: Obligation[] = [];

  constructor(private apiService: ApiService) {}

  ngOnInit() {
    this.checkConnection();
    this.loadStates();
    this.loadObligations();
  }

  async checkConnection() {
    try {
      const response = await this.apiService.getHealth().toPromise();
      this.connectionStatus = 'success';
      this.statusMessage = `✅ Conectado! ${response.obligations_count} obrigações no banco`;
    } catch (error) {
      this.connectionStatus = 'error';
      this.statusMessage = '❌ Erro de conexão. Verifique se o backend está rodando.';
    }
  }

  async loadStates() {
    try {
      this.states = await this.apiService.getStates().toPromise() || [];
    } catch (error) {
      console.error('Erro ao carregar estados:', error);
    }
  }

  async onStateChange() {
    this.selectedCounty = '';
    this.selectedCity = '';
    this.counties = [];
    this.cities = [];
    
    if (this.selectedState) {
      try {
        this.counties = await this.apiService.getCounties(this.selectedState).toPromise() || [];
      } catch (error) {
        console.error('Erro ao carregar condados:', error);
      }
    }
  }

  async onCountyChange() {
    this.selectedCity = '';
    this.cities = [];
    
    if (this.selectedCounty && this.selectedState) {
      try {
        this.cities = await this.apiService.getCities(this.selectedState, this.selectedCounty).toPromise() || [];
      } catch (error) {
        console.error('Erro ao carregar cidades:', error);
      }
    }
  }

  onCityChange() {
    // Implementar se necessário
  }

  onDateRangeChange() {
    // Implementar se necessário
  }

  clearFilters() {
    this.selectedState = '';
    this.selectedCounty = '';
    this.selectedCity = '';
    this.selectedDateRange = '';
    this.counties = [];
    this.cities = [];
    this.applyFilters();
  }

  async applyFilters() {
    this.loading = true;
    
    const filters: any = {};
    if (this.selectedState) filters.state = this.selectedState;
    if (this.selectedCounty) filters.county = this.selectedCounty;
    if (this.selectedCity) filters.city = this.selectedCity;
    if (this.selectedDateRange) filters.date_range = this.selectedDateRange;
    
    try {
      this.obligations = await this.apiService.getObligations(filters).toPromise() || {
        federal: [],
        state: [],
        county: [],
        municipality: []
      };
      
      this.combineObligations();
    } catch (error) {
      console.error('Erro ao carregar obrigações:', error);
    } finally {
      this.loading = false;
    }
  }

  async loadObligations() {
    await this.applyFilters();
  }

  combineObligations() {
    this.allObligations = [
      ...this.obligations.federal.map(ob => ({...ob, level: 'federal'})),
      ...this.obligations.state.map(ob => ({...ob, level: 'state'})),
      ...this.obligations.county.map(ob => ({...ob, level: 'county'})),
      ...this.obligations.municipality.map(ob => ({...ob, level: 'municipality'}))
    ];
    
    // Ordenar por data
    this.allObligations.sort((a, b) => {
      if (!a.due_date) return 1;
      if (!b.due_date) return -1;
      return new Date(a.due_date).getTime() - new Date(b.due_date).getTime();
    });
  }

  formatDate(dateString: string): string {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric'
    });
  }

  getLevelIcon(level: string): string {
    const icons: { [key: string]: string } = {
      federal: 'flag',
      state: 'place',
      county: 'location_city',
      municipality: 'business'
    };
    return icons[level] || 'event';
  }

  getLevelName(level: string): string {
    const names: { [key: string]: string } = {
      federal: 'Federal',
      state: 'Estadual',
      county: 'Condado',
      municipality: 'Municipal'
    };
    return names[level] || level;
  }
}
