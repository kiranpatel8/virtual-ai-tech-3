import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface DeviceIdentificationResponse {
  filename: string;
  file_size: number;
  model_used: string;
  status: string;
  predictions?: Array<{
    label: string;
    score: number;
  }>;
  top_prediction?: {
    label: string;
    score: number;
  };
  confidence?: number;
  message?: string;
  estimated_time?: number;
  // Problem detection fields
  problem_detected?: boolean;
  problem_description?: string;
  dispatch_note?: string;
}

export interface HealthResponse {
  status: string;
  service: string;
  huggingface_configured: boolean;
  model?: string;
}

@Injectable({
  providedIn: 'root'
})
export class DeviceIdentifierService {
  private apiUrl = environment.apiUrl;

  constructor(private http: HttpClient) { }

  /**
   * Check if the API service is healthy and configured
   */
  checkHealth(): Observable<HealthResponse> {
    return this.http.get<HealthResponse>(`${this.apiUrl}/health`);
  }

  /**
   * Send image to the API for device identification
   * @param imageBlob The image file to identify
   * @param filename The filename to send to the API
   */
  identifyDevice(imageBlob: Blob, filename: string): Observable<DeviceIdentificationResponse> {
    const formData = new FormData();
    formData.append('file', imageBlob, filename);

    return this.http.post<DeviceIdentificationResponse>(
      `${this.apiUrl}/identify`, 
      formData
    );
  }

  /**
   * Convert base64 image data to Blob
   * @param base64Data Base64 encoded image data
   * @param contentType MIME type of the image
   */
  base64ToBlob(base64Data: string, contentType: string = 'image/jpeg'): Blob {
    const byteCharacters = atob(base64Data);
    const byteNumbers = new Array(byteCharacters.length);
    
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i);
    }
    
    const byteArray = new Uint8Array(byteNumbers);
    return new Blob([byteArray], { type: contentType });
  }
}
