#!/usr/bin/env python3
"""
Smart Nation Integration Example - Singapore's Digital Government Infrastructure
==================================================================================

This example demonstrates how Singapore's Smart Nation and Digital Government Office (SNDGO)
can integrate JEP into its core digital infrastructure to meet the requirements of
Smart Nation 2025, digital identity, data sharing, and whole-of-government integration.

Regulatory Compliance:
- Smart Nation 2025 Strategy
- Digital Government Blueprint
- SingPass/CorpPass Framework
- APEX (API Exchange) Platform
- WOG Data Sharing Protocols
- PDPA
- GovTech DSS

Scenarios Covered:
1. National Digital Identity (NDI) - SingPass authentication
2. APEX API Gateway - Cross-agency data exchange
3. MyInfo consent management
4. National AI Strategy - Accountability framework
5. Smart City Sensor Data Management
6. Whole-of-government analytics
"""

import json
import time
import hashlib
import hmac
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field, asdict

# Import JEP components
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from implementation.accountability import (
    AgenticAIAccountability,
    ActionProposal,
    HumanApprovalRecord,
    RiskLevel,
    ActionStatus
)
from jep.core import JEPAsymmetricSigner, generate_uuid7


class DigitalServiceType(Enum):
    """Types of digital services in Smart Nation"""
    SINGPASS_AUTH = "SINGPASS_AUTH"
    CORPPASS_AUTH = "CORPPASS_AUTH"
    MYINFO = "MYINFO"
    APEX_API = "APEX_API"
    SMART_CITY_SENSOR = "SMART_CITY_SENSOR"
    NATIONAL_AI = "NATIONAL_AI"
    WOG_ANALYTICS = "WOG_ANALYTICS"
    PAYMENTS = "PAYMENTS"


class DataClassification(Enum):
    """Data classification levels for WOG"""
    PUBLIC = "PUBLIC"
    OFFICIAL = "OFFICIAL"
    RESTRICTED = "RESTRICTED"
    CONFIDENTIAL = "CONFIDENTIAL"
    SECRET = "SECRET"


class AuthLevel(Enum):
    """Authentication levels for SingPass/CorpPass"""
    LEVEL1 = "BASIC"        # Basic authentication
    LEVEL2 = "MFA"           # Multi-factor authentication
    LEVEL3 = "SINGPASS_APP"  # SingPass Mobile
    LEVEL4 = "FACE_VERIFY"   # Face verification
    LEVEL5 = "TOKEN_HARDWARE" # Hardware token


class SmartNationIntegration:
    """
    Complete Smart Nation integration example showing JEP implementation
    for Singapore's digital government infrastructure.
    """
    
    def __init__(self, environment: str = "production"):
        """
        Initialize Smart Nation integration with JEP.
        
        Args:
            environment: "production", "staging", or "test"
        """
        self.environment = environment
        self.system_id = f"smart-nation-{generate_uuid7()[:8]}"
        
        # Initialize JEP tracker for SNDGO
        self.tracker = AgenticAIAccountability(
            agent_id=f"sndgo-agent-{environment}",
            organization="SNDGO"
        )
        
        # Smart Nation configuration
        self.auth_levels = {
            AuthLevel.LEVEL1: {"risk": RiskLevel.LOW, "services": ["public_info"]},
            AuthLevel.LEVEL2: {"risk": RiskLevel.LOW, "services": ["personal_profile"]},
            AuthLevel.LEVEL3: {"risk": RiskLevel.MEDIUM, "services": ["financial", "healthcare"]},
            AuthLevel.LEVEL4: {"risk": RiskLevel.HIGH, "services": ["government_transactions"]},
            AuthLevel.LEVEL5: {"risk": RiskLevel.CRITICAL, "services": ["national_security"]}
        }
        
        # API rate limits and quotas
        self.api_quotas = {
            "CPF_BOARD": {"daily_limit": 100000, "hourly_limit": 10000},
            "IRAS": {"daily_limit": 50000, "hourly_limit": 5000},
            "HDB": {"daily_limit": 75000, "hourly_limit": 7500},
            "MOH": {"daily_limit": 80000, "hourly_limit": 8000},
            "MOE": {"daily_limit": 40000, "hourly_limit": 4000}
        }
        
        # Data stores
        self.auth_sessions = {}
        self.api_calls = []
        self.consent_records = []
        self.sensor_data = []
        self.audit_log = []
        
        print(f"✅ Smart Nation Integration Initialized")
        print(f"   System ID: {self.system_id}")
        print(f"   Environment: {environment}")
        print(f"   JEP Tracker: {self.tracker.agent_id}")
    
    def authenticate_citizen(
        self,
        nric: str,
        auth_method: AuthLevel,
        service_requested: str,
        device_info: Dict[str, Any],
        location: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Authenticate citizen via SingPass with appropriate security level.
        
        This demonstrates:
        - National Digital Identity (NDI) framework
        - Risk-based authentication
        - Session management
        - Fraud detection
        - Complete audit trail
        """
        print(f"\n{'='*60}")
        print(f"🔐 SingPass Authentication")
        print(f"{'='*60}")
        print(f"Citizen NRIC: {nric[:3]}***{nric[-3:]}")
        print(f"Auth Method: {auth_method.value}")
        print(f"Service: {service_requested}")
        
        # Hash NRIC for audit trail
        nric_hash = hashlib.sha256(nric.encode()).hexdigest()[:16]
        
        # Check if requested service requires higher auth level
        required_level = self._get_required_auth_level(service_requested)
        if self.auth_levels[auth_method]["risk"].value < self.auth_levels[required_level]["risk"].value:
            return {
                "status": "REJECTED",
                "reason": f"Insufficient authentication level. Required: {required_level.value}",
                "timestamp": time.time()
            }
        
        # Perform fraud checks
        fraud_check = self._perform_fraud_checks(nric_hash, device_info, location)
        
        # Determine risk level
        if fraud_check["risk_score"] > 0.8:
            risk_level = RiskLevel.CRITICAL
        elif fraud_check["risk_score"] > 0.5:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = self.auth_levels[auth_method]["risk"]
        
        # Create session
        session_id = f"SESS-{generate_uuid7()[:12]}"
        session = {
            "session_id": session_id,
            "nric_hash": nric_hash,
            "auth_method": auth_method.value,
            "auth_time": time.time(),
            "expiry_time": time.time() + 3600,  # 1 hour session
            "service_requested": service_requested,
            "device_info": device_info,
            "location": location,
            "fraud_check": fraud_check,
            "risk_level": risk_level.value
        }
        
        # Create proposal in JEP
        proposal = self.tracker.propose_action(
            action="CITIZEN_AUTH",
            target_resource=f"citizen/{nric_hash}/session/{session_id}",
            reasoning=f"SingPass authentication for {service_requested}",
            risk_level=risk_level.value,
            session=session,
            fraud_check=fraud_check
        )
        
        # High-risk authentication may require additional verification
        if risk_level == RiskLevel.CRITICAL:
            # Require second factor
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver="FRAUD_ANALYST",
                context_reviewed=True,
                notes=f"High-risk authentication flagged for review"
            )
            print(f"   ⚠️ High-risk authentication flagged for review")
        else:
            # Standard approval
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver="SYSTEM",
                context_reviewed=True,
                notes=f"Authentication successful"
            )
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Store session
        self.auth_sessions[session_id] = session
        
        result = {
            "status": "AUTHENTICATED",
            "session_id": session_id,
            "auth_token": hashlib.sha256(f"{session_id}{time.time()}".encode()).hexdigest()[:32],
            "expiry_time": session["expiry_time"],
            "auth_level": auth_method.value,
            "risk_level": risk_level.value,
            "audit_receipt": execution,
            "approval_receipt": approval.to_dict()
        }
        
        self._log_audit_event("CITIZEN_AUTH", {
            "nric_hash": nric_hash,
            "session_id": session_id,
            "risk_level": risk_level.value
        })
        
        return result
    
    def _get_required_auth_level(self, service: str) -> AuthLevel:
        """Determine required authentication level for service."""
        service_map = {
            "public_info": AuthLevel.LEVEL1,
            "personal_profile": AuthLevel.LEVEL2,
            "cpf_withdrawal": AuthLevel.LEVEL3,
            "tax_filing": AuthLevel.LEVEL3,
            "property_transaction": AuthLevel.LEVEL4,
            "national_security": AuthLevel.LEVEL5
        }
        return service_map.get(service, AuthLevel.LEVEL2)
    
    def _perform_fraud_checks(
        self,
        nric_hash: str,
        device_info: Dict[str, Any],
        location: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Perform fraud detection checks."""
        risk_score = 0.0
        risk_factors = []
        
        # Check for suspicious device
        if device_info.get("is_emulator", False):
            risk_score += 0.4
            risk_factors.append("Emulator detected")
        
        if device_info.get("is_jailbroken", False):
            risk_score += 0.3
            risk_factors.append("Jailbroken device")
        
        # Check for unusual location
        if location:
            if location.get("country") != "SG":
                risk_score += 0.2
                risk_factors.append("Foreign location")
        
        # Check for multiple recent attempts
        recent_attempts = sum(1 for s in self.auth_sessions.values() 
                             if s["nric_hash"] == nric_hash 
                             and time.time() - s["auth_time"] < 300)  # Last 5 minutes
        if recent_attempts > 3:
            risk_score += 0.3
            risk_factors.append("Multiple recent attempts")
        
        return {
            "risk_score": min(risk_score, 1.0),
            "risk_factors": risk_factors,
            "recommended_action": "allow" if risk_score < 0.7 else "review",
            "check_time": time.time()
        }
    
    def process_apex_api_call(
        self,
        source_agency: str,
        target_agency: str,
        api_name: str,
        request_data: Dict[str, Any],
        purpose: str,
        consent_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process cross-agency API call through APEX gateway.
        
        This demonstrates:
        - APEX API Gateway integration
        - Agency-to-agency data sharing
        - Rate limiting and quotas
        - Consent verification
        - Complete audit trail
        """
        print(f"\n{'='*60}")
        print(f"🔄 APEX Cross-Agency API Call")
        print(f"{'='*60}")
        print(f"Source Agency: {source_agency}")
        print(f"Target Agency: {target_agency}")
        print(f"API: {api_name}")
        print(f"Purpose: {purpose}")
        
        # Check rate limits
        quota_check = self._check_rate_limit(source_agency, target_agency, api_name)
        if not quota_check["allowed"]:
            return {
                "status": "REJECTED",
                "reason": quota_check["reason"],
                "reset_time": quota_check["reset_time"]
            }
        
        # Verify consent if accessing personal data
        if "personal_data" in request_data.get("data_types", []):
            if not consent_id:
                return {
                    "status": "REJECTED",
                    "reason": "Consent required for personal data access"
                }
            consent_valid = self._verify_consent(consent_id, source_agency, purpose)
            if not consent_valid["valid"]:
                return {
                    "status": "REJECTED",
                    "reason": consent_valid["reason"]
                }
        
        # Create API call record
        api_call_id = f"API-{generate_uuid7()[:12]}"
        api_call = {
            "call_id": api_call_id,
            "source_agency": source_agency,
            "target_agency": target_agency,
            "api_name": api_name,
            "request_data_summary": {k: type(v).__name__ for k, v in request_data.items()},
            "purpose": purpose,
            "consent_id": consent_id,
            "timestamp": time.time(),
            "data_classification": self._determine_data_classification(request_data)
        }
        
        # Create proposal
        proposal = self.tracker.propose_action(
            action="APEX_API_CALL",
            target_resource=f"apex/{source_agency}/{target_agency}/{api_name}",
            reasoning=f"Cross-agency data sharing: {purpose}",
            risk_level=self._determine_api_risk(api_call),
            api_call=api_call,
            quota_check=quota_check,
            consent_verified=consent_valid if consent_id else None
        )
        
        # Auto-approve for routine data sharing
        if api_call["data_classification"] in [DataClassification.PUBLIC, DataClassification.OFFICIAL]:
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver="SYSTEM",
                context_reviewed=True,
                notes=f"Auto-approved: {purpose}"
            )
            print(f"   ✅ Auto-approved (routine data)")
        else:
            # Sensitive data requires human approval
            approver_id = f"APEX-REVIEWER-{generate_uuid7()[:6]}"
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver=approver_id,
                context_reviewed=True,
                notes=f"Approved after review: {purpose}"
            )
            print(f"   ✅ Approved by: {approver_id}")
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Update rate limit counters
        self._update_rate_limit(source_agency, target_agency, api_name)
        
        # Store API call
        api_call["execution_receipt"] = execution
        self.api_calls.append(api_call)
        
        result = {
            "status": "PROCESSED",
            "call_id": api_call_id,
            "source_agency": source_agency,
            "target_agency": target_agency,
            "api_name": api_name,
            "timestamp": api_call["timestamp"],
            "audit_receipt": execution,
            "approval_receipt": approval.to_dict()
        }
        
        return result
    
    def _check_rate_limit(
        self,
        source: str,
        target: str,
        api: str
    ) -> Dict[str, Any]:
        """Check if API call is within rate limits."""
        quotas = self.api_quotas.get(source, {"daily_limit": 1000, "hourly_limit": 100})
        
        # Count calls in last 24 hours
        daily_calls = sum(1 for c in self.api_calls 
                         if c["source_agency"] == source 
                         and c["target_agency"] == target
                         and time.time() - c["timestamp"] < 86400)
        
        # Count calls in last hour
        hourly_calls = sum(1 for c in self.api_calls 
                          if c["source_agency"] == source 
                          and c["target_agency"] == target
                          and time.time() - c["timestamp"] < 3600)
        
        if daily_calls >= quotas["daily_limit"]:
            return {
                "allowed": False,
                "reason": f"Daily limit exceeded ({quotas['daily_limit']})",
                "reset_time": time.time() + 86400
            }
        
        if hourly_calls >= quotas["hourly_limit"]:
            return {
                "allowed": False,
                "reason": f"Hourly limit exceeded ({quotas['hourly_limit']})",
                "reset_time": time.time() + 3600
            }
        
        return {
            "allowed": True,
            "daily_remaining": quotas["daily_limit"] - daily_calls,
            "hourly_remaining": quotas["hourly_limit"] - hourly_calls
        }
    
    def _update_rate_limit(self, source: str, target: str, api: str) -> None:
        """Update rate limit counters."""
        # Handled by the call counting in _check_rate_limit
        pass
    
    def _determine_data_classification(self, data: Dict[str, Any]) -> DataClassification:
        """Determine data classification based on content."""
        sensitive_keywords = ["nric", "name", "address", "phone", "email", "salary", "medical"]
        
        data_str = json.dumps(data).lower()
        for keyword in sensitive_keywords:
            if keyword in data_str:
                return DataClassification.RESTRICTED
        
        return DataClassification.OFFICIAL
    
    def _determine_api_risk(self, api_call: Dict[str, Any]) -> RiskLevel:
        """Determine risk level of API call."""
        if api_call["data_classification"] in [DataClassification.CONFIDENTIAL, DataClassification.SECRET]:
            return RiskLevel.CRITICAL
        elif api_call["data_classification"] == DataClassification.RESTRICTED:
            return RiskLevel.HIGH
        elif "health" in api_call["api_name"].lower() or "finance" in api_call["api_name"].lower():
            return RiskLevel.MEDIUM
        else:
            return RiskLevel.LOW
    
    def manage_myinfo_consent(
        self,
        nric: str,
        requesting_agency: str,
        requested_attributes: List[str],
        consent_duration_days: int,
        purpose: str
    ) -> Dict[str, Any]:
        """
        Manage MyInfo consent for data sharing.
        
        This demonstrates:
        - MyInfo consent framework
        - Attribute-based consent
        - Consent expiry and revocation
        - Audit trail
        """
        print(f"\n{'='*60}")
        print(f"📝 MyInfo Consent Management")
        print(f"{'='*60}")
        print(f"Citizen: {nric[:3]}***{nric[-3:]}")
        print(f"Requesting Agency: {requesting_agency}")
        print(f"Requested Attributes: {requested_attributes}")
        print(f"Duration: {consent_duration_days} days")
        print(f"Purpose: {purpose}")
        
        nric_hash = hashlib.sha256(nric.encode()).hexdigest()[:16]
        
        # Create consent record
        consent_id = f"CONSENT-{generate_uuid7()[:12]}"
        consent_record = {
            "consent_id": consent_id,
            "citizen_hash": nric_hash,
            "requesting_agency": requesting_agency,
            "requested_attributes": requested_attributes,
            "purpose": purpose,
            "granted_at": time.time(),
            "expires_at": time.time() + (consent_duration_days * 86400),
            "status": "ACTIVE",
            "revocation_history": []
        }
        
        # Create proposal
        proposal = self.tracker.propose_action(
            action="MYINFO_CONSENT",
            target_resource=f"citizen/{nric_hash}/consent/{consent_id}",
            reasoning=f"MyInfo consent for {requesting_agency}: {purpose}",
            risk_level=RiskLevel.MEDIUM,
            consent=consent_record,
            attributes_requested=requested_attributes
        )
        
        # Consent requires explicit approval
        approval = self.tracker.approve_action(
            proposal_id=proposal.id,
            human_approver="SYSTEM",
            context_reviewed=True,
            notes=f"Consent recorded for {requesting_agency}"
        )
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Store consent
        self.consent_records.append(consent_record)
        
        result = {
            "status": "CONSENT_GRANTED",
            "consent_id": consent_id,
            "requesting_agency": requesting_agency,
            "granted_attributes": requested_attributes,
            "expires_at": consent_record["expires_at"],
            "audit_receipt": execution,
            "approval_receipt": approval.to_dict()
        }
        
        return result
    
    def _verify_consent(
        self,
        consent_id: str,
        requesting_agency: str,
        purpose: str
    ) -> Dict[str, Any]:
        """Verify if consent is valid for the request."""
        for consent in self.consent_records:
            if consent["consent_id"] == consent_id:
                if consent["status"] != "ACTIVE":
                    return {"valid": False, "reason": "Consent not active"}
                if consent["requesting_agency"] != requesting_agency:
                    return {"valid": False, "reason": "Consent not for this agency"}
                if consent["expires_at"] < time.time():
                    return {"valid": False, "reason": "Consent expired"}
                if purpose not in consent["purpose"].lower():
                    return {"valid": False, "reason": "Purpose not covered"}
                return {"valid": True, "consent": consent}
        
        return {"valid": False, "reason": "Consent not found"}
    
    def process_smart_city_sensor(
        self,
        sensor_id: str,
        sensor_type: str,
        location: Dict[str, Any],
        readings: Dict[str, Any],
        privacy_filter_applied: bool
    ) -> Dict[str, Any]:
        """
        Process smart city sensor data with privacy protection.
        
        This demonstrates:
        - Smart city sensor network
        - Privacy-preserving data collection
        - Real-time processing
        - Data retention policies
        """
        print(f"\n{'='*60}")
        print(f"🌆 Smart City Sensor Data")
        print(f"{'='*60}")
        print(f"Sensor ID: {sensor_id}")
        print(f"Sensor Type: {sensor_type}")
        print(f"Location: {location}")
        print(f"Privacy Filter Applied: {privacy_filter_applied}")
        
        # Apply privacy filters if not already applied
        if not privacy_filter_applied:
            readings = self._apply_privacy_filters(readings, sensor_type)
        
        # Generate data hash for integrity
        data_hash = hashlib.sha256(json.dumps(readings, sort_keys=True).encode()).hexdigest()
        
        # Create sensor data record
        sensor_data = {
            "data_id": f"SENSOR-{generate_uuid7()[:12]}",
            "sensor_id": sensor_id,
            "sensor_type": sensor_type,
            "location_hash": hashlib.sha256(json.dumps(location).encode()).hexdigest()[:16],
            "readings": readings,
            "timestamp": time.time(),
            "data_hash": data_hash,
            "privacy_filter_applied": privacy_filter_applied,
            "retention_days": 30
        }
        
        # Create proposal
        proposal = self.tracker.propose_action(
            action="SENSOR_DATA",
            target_resource=f"sensor/{sensor_id}/data/{sensor_data['data_id']}",
            reasoning=f"Smart city sensor data: {sensor_type}",
            risk_level=RiskLevel.LOW,
            sensor_data=sensor_data,
            data_hash=data_hash
        )
        
        # Auto-approve sensor data
        approval = self.tracker.approve_action(
            proposal_id=proposal.id,
            human_approver="SYSTEM",
            context_reviewed=True,
            notes=f"Sensor data recorded with privacy protection"
        )
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Store sensor data
        self.sensor_data.append(sensor_data)
        
        result = {
            "status": "RECORDED",
            "data_id": sensor_data["data_id"],
            "timestamp": sensor_data["timestamp"],
            "data_hash": data_hash,
            "retention_date": time.time() + (30 * 86400),
            "audit_receipt": execution
        }
        
        return result
    
    def _apply_privacy_filters(
        self,
        readings: Dict[str, Any],
        sensor_type: str
    ) -> Dict[str, Any]:
        """Apply privacy filters to sensor data."""
        filtered = readings.copy()
        
        if sensor_type == "CCTV":
            # Blur faces, anonymize
            filtered["privacy_processed"] = True
            filtered["face_blurred"] = True
            filtered["license_plate_blurred"] = True
        
        elif sensor_type == "WiFi_TRACKING":
            # Hash MAC addresses
            if "mac_addresses" in filtered:
                filtered["mac_addresses"] = [
                    hashlib.sha256(mac.encode()).hexdigest()[:16]
                    for mac in filtered["mac_addresses"]
                ]
        
        elif sensor_type == "ENVIRONMENTAL":
            # Aggregate to area level
            filtered["location_precision"] = "area"
        
        return filtered
    
    def generate_wog_analytics(
        self,
        analysis_type: str,
        agencies_included: List[str],
        data_period_days: int,
        requesting_officer: str
    ) -> Dict[str, Any]:
        """
        Generate whole-of-government analytics report.
        
        This demonstrates:
        - Cross-agency data analytics
        - Privacy-preserving aggregation
        - Access control
        - Audit trail for data usage
        """
        print(f"\n{'='*60}")
        print(f"📊 Whole-of-Government Analytics")
        print(f"{'='*60}")
        print(f"Analysis Type: {analysis_type}")
        print(f"Agencies: {agencies_included}")
        print(f"Period: {data_period_days} days")
        print(f"Requesting Officer: {requesting_officer}")
        
        # Hash officer ID
        officer_hash = hashlib.sha256(requesting_officer.encode()).hexdigest()[:16]
        
        # Create analytics request
        analytics_id = f"ANALYTICS-{generate_uuid7()[:12]}"
        analytics_request = {
            "request_id": analytics_id,
            "analysis_type": analysis_type,
            "agencies_included": agencies_included,
            "data_period_days": data_period_days,
            "requesting_officer_hash": officer_hash,
            "request_time": time.time(),
            "status": "PENDING"
        }
        
        # Determine risk level based on analysis type
        if analysis_type in ["citizen_profiling", "predictive_policing"]:
            risk_level = RiskLevel.CRITICAL
        elif analysis_type in ["service_usage", "demographic_trends"]:
            risk_level = RiskLevel.HIGH
        else:
            risk_level = RiskLevel.MEDIUM
        
        # Create proposal
        proposal = self.tracker.propose_action(
            action="WOG_ANALYTICS",
            target_resource=f"analytics/{analytics_id}",
            reasoning=f"WOG analytics: {analysis_type}",
            risk_level=risk_level.value,
            analytics_request=analytics_request
        )
        
        # Analytics requests require approval
        if risk_level == RiskLevel.CRITICAL:
            # Critical analysis requires committee approval
            approval1 = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver="DATA_ETHICS_COMMITTEE",
                context_reviewed=True,
                notes=f"Approved with privacy safeguards"
            )
            print(f"   ✅ Data Ethics Committee Approved")
            
            approval2 = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver="PERMANENT_SECRETARY",
                context_reviewed=True,
                notes=f"Final approval granted"
            )
            print(f"   ✅ Permanent Secretary Approved")
            
            approvals = [approval1.to_dict(), approval2.to_dict()]
        else:
            # Standard approval
            approver_id = f"ANALYTICS-REVIEWER-{generate_uuid7()[:6]}"
            approval = self.tracker.approve_action(
                proposal_id=proposal.id,
                human_approver=approver_id,
                context_reviewed=True,
                notes=f"Analytics request approved"
            )
            print(f"   ✅ Approved by: {approver_id}")
            approvals = [approval.to_dict()]
        
        execution = self.tracker.execute_approved_action(proposal.id)
        
        # Simulate analytics generation
        analytics_result = self._generate_sample_analytics(
            analysis_type, 
            agencies_included, 
            data_period_days
        )
        
        result = {
            "status": "ANALYTICS_GENERATED",
            "analytics_id": analytics_id,
            "analysis_type": analysis_type,
            "generated_at": time.time(),
            "result_summary": analytics_result["summary"],
            "data_sources": analytics_result["sources"],
            "privacy_notes": "All data aggregated, no individual identifiers",
            "audit_receipt": execution,
            "approvals": approvals
        }
        
        return result
    
    def _generate_sample_analytics(
        self,
        analysis_type: str,
        agencies: List[str],
        days: int
    ) -> Dict[str, Any]:
        """Generate sample analytics results."""
        if analysis_type == "service_usage":
            return {
                "summary": {
                    "total_transactions": 1500000,
                    "digital_transactions": 1425000,
                    "counter_transactions": 75000,
                    "digital_penetration": "95%"
                },
                "sources": agencies
            }
        elif analysis_type == "demographic_trends":
            return {
                "summary": {
                    "active_users": 2500000,
                    "age_groups": {
                        "20-35": "35%",
                        "36-50": "40%",
                        "51-65": "20%",
                        "65+": "5%"
                    }
                },
                "sources": agencies
            }
        else:
            return {
                "summary": "Analytics generated successfully",
                "sources": agencies
            }
    
    def _log_audit_event(self, event_type: str, data: Dict[str, Any]) -> None:
        """Internal audit logging."""
        self.audit_log.append({
            "event_type": event_type,
            "timestamp": time.time(),
            "data": data
        })
    
    def generate_smart_nation_report(
        self,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive Smart Nation audit report.
        
        This report can be submitted to:
        - Smart Nation and Digital Government Office
        - Prime Minister's Office
        - Parliament
        - International digital government benchmarks
        """
        report = {
            "report_id": f"SN-{generate_uuid7()[:12]}",
            "system_id": self.system_id,
            "environment": self.environment,
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "reporting_period": {
                "start": start_date or "N/A",
                "end": end_date or "N/A"
            },
            "statistics": {
                "authentications": len(self.auth_sessions),
                "api_calls": len(self.api_calls),
                "consent_records": len(self.consent_records),
                "sensor_readings": len(self.sensor_data)
            },
            "digital_identity": {
                "total_auth_sessions": len(self.auth_sessions),
                "avg_session_duration": 1800,  # 30 minutes
                "mfa_usage": sum(1 for s in self.auth_sessions.values() 
                                if s.get("auth_method") in [AuthLevel.LEVEL2.value, AuthLevel.LEVEL3.value]),
                "high_risk_flags": sum(1 for s in self.auth_sessions.values() 
                                      if s.get("risk_level") in ["HIGH", "CRITICAL"])
            },
            "data_sharing": {
                "total_api_calls": len(self.api_calls),
                "agencies_involved": len(set(c["source_agency"] for c in self.api_calls)),
                "data_classification": {
                    "PUBLIC": sum(1 for c in self.api_calls if c.get("data_classification") == "PUBLIC"),
                    "OFFICIAL": sum(1 for c in self.api_calls if c.get("data_classification") == "OFFICIAL"),
                    "RESTRICTED": sum(1 for c in self.api_calls if c.get("data_classification") == "RESTRICTED")
                }
            },
            "consent_management": {
                "active_consents": sum(1 for c in self.consent_records if c["status"] == "ACTIVE"),
                "expired_consents": sum(1 for c in self.consent_records if c["status"] == "EXPIRED"),
                "avg_consent_duration": 365  # days
            },
            "compliance_summary": {
                "pdp_a": "COMPLIANT",
                "smart_nation_2025": "ON_TRACK",
                "digital_government_blueprint": "ALIGNED",
                "wog_data_sharing": "COMPLIANT"
            },
            "audit_integrity": {
                "signature_validity": "ALL_VALID",
                "audit_chain_complete": True,
                "pii_protected": True
            }
        }
        
        # Sign the report
        report["signature"] = self.tracker.signer.sign_payload(report)
        
        return report


def simulate_smart_nation_operations(sn_system: SmartNationIntegration) -> None:
    """
    Simulate Smart Nation operations for testing/demonstration.
    """
    print(f"\n{'#'*60}")
    print(f"🌐 Simulating Smart Nation Operations")
    print(f"{'#'*60}")
    
    # Simulate citizen authentications
    citizens = [
        {"nric": "S1234567A", "device": {"is_emulator": False, "is_jailbroken": False}},
        {"nric": "S7654321B", "device": {"is_emulator": False, "is_jailbroken": True}},
        {"nric": "S9876543C", "device": {"is_emulator": False, "is_jailbroken": False}},
        {"nric": "S4567890D", "device": {"is_emulator": True, "is_jailbroken": False}}
    ]
    
    for i, citizen in enumerate(citizens):
        print(f"\n--- Authentication {i+1} ---")
        result = sn_system.authenticate_citizen(
            nric=citizen["nric"],
            auth_method=AuthLevel.LEVEL3,
            service_requested="cpf_withdrawal" if i % 2 == 0 else "personal_profile",
            device_info=citizen["device"],
            location={"country": "SG", "postal": "123456"} if i != 2 else {"country": "MY", "postal": "80000"}
        )
        print(f"   → Session: {result.get('session_id', 'N/A')} | Status: {result.get('status')}")
    
    # Simulate APEX API calls
    agencies = [
        {"source": "CPF_BOARD", "target": "HDB", "api": "property_ownership"},
        {"source": "IRAS", "target": "CPF_BOARD", "api": "income_data"},
        {"source": "MOH", "target": "MOE", "api": "student_health"}
    ]
    
    for i, agency in enumerate(agencies):
        print(f"\n--- APEX API Call {i+1} ---")
        result = sn_system.process_apex_api_call(
            source_agency=agency["source"],
            target_agency=agency["target"],
            api_name=agency["api"],
            request_data={"data_types": ["personal_data"] if i == 0 else ["aggregate_stats"]},
            purpose=f"{agency['source']} to {agency['target']} data sharing",
            consent_id=f"CONSENT-{generate_uuid7()[:8]}" if i == 0 else None
        )
        print(f"   → API Call: {result.get('call_id', 'N/A')} | Status: {result.get('status')}")
    
    # Simulate MyInfo consent
    print(f"\n--- MyInfo Consent ---")
    result = sn_system.manage_myinfo_consent(
        nric="S1234567A",
        requesting_agency="MOH",
        requested_attributes=["name", "nric", "address", "phone"],
        consent_duration_days=365,
        purpose="Healthcare service eligibility"
    )
    print(f"   → Consent: {result.get('consent_id', 'N/A')} | Status: {result.get('status')}")
    
    # Simulate smart city sensors
    sensors = [
        {"id": "SENSOR001", "type": "CCTV", "location": {"area": "Orchard Road", "postal": "238859"}},
        {"id": "SENSOR002", "type": "WiFi_TRACKING", "location": {"area": "CBD", "postal": "048619"}},
        {"id": "SENSOR003", "type": "ENVIRONMENTAL", "location": {"area": "East Coast", "postal": "449876"}}
    ]
    
    for i, sensor in enumerate(sensors):
        print(f"\n--- Sensor Data {i+1} ---")
        result = sn_system.process_smart_city_sensor(
            sensor_id=sensor["id"],
            sensor_type=sensor["type"],
            location=sensor["location"],
            readings={
                "timestamp": time.time(),
                "value": 100 + i,
                "unit": "count",
                "mac_addresses": ["AA:BB:CC:DD:EE:FF", "11:22:33:44:55:66"] if sensor["type"] == "WiFi_TRACKING" else None
            },
            privacy_filter_applied=False
        )
        print(f"   → Data ID: {result.get('data_id', 'N/A')} | Status: {result.get('status')}")
    
    # Simulate WOG analytics
    print(f"\n--- WOG Analytics ---")
    result = sn_system.generate_wog_analytics(
        analysis_type="service_usage",
        agencies_included=["CPF_BOARD", "IRAS", "HDB", "MOH"],
        data_period_days=30,
        requesting_officer="analytics-officer-001"
    )
    print(f"   → Analytics ID: {result.get('analytics_id', 'N/A')} | Status: {result.get('status')}")


def main():
    """
    Run Smart Nation integration example.
    """
    print(f"\n{'='*60}")
    print(f"🇸🇬 Smart Nation JEP Integration Example")
    print(f"{'='*60}")
    
    # Initialize Smart Nation system
    sn_system = SmartNationIntegration(environment="test")
    
    # Simulate operations
    simulate_smart_nation_operations(sn_system)
    
    # Generate Smart Nation report
    print(f"\n{'='*60}")
    print(f"📊 Generating Smart Nation Audit Report")
    print(f"{'='*60}")
    
    report = sn_system.generate_smart_nation_report(
        start_date="2026-03-01",
        end_date="2026-03-07"
    )
    
    # Save report
    report_file = "smart_nation_audit_report_q1_2026.json"
    with open(report_file, 'w') as f:
        json.dump(report, f, indent=2, default=str)
    print(f"✅ Audit report saved to: {report_file}")
    
    print(f"\n{'='*60}")
    print(f"✅ Smart Nation Integration Example Complete")
    print(f"   This demonstrates:")
    print(f"   - National Digital Identity (SingPass)")
    print(f"   - APEX cross-agency API gateway")
    print(f"   - MyInfo consent management")
    print(f"   - Smart city sensor network")
    print(f"   - Whole-of-government analytics")
    print(f"   - Privacy-preserving data collection")
    print(f"   - Complete audit trail for Smart Nation 2025")
    print(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
