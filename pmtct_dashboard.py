import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# Set page configuration
st.set_page_config(
    page_title="PMTCT Dashboard - Nigeria",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Nigerian colors (Green and White) and larger, bolder fonts
st.markdown("""
<style>
    .main-header {
        font-size: 3rem !important;
        color: #008751 !important;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 900 !important;
    }
    .sub-header {
        color: #008751;
        border-left: 6px solid #008751;
        padding-left: 15px;
        margin-top: 25px;
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    .section-header {
        background: linear-gradient(135deg, #008751 0%, #87CEEB 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        margin: 15px 0;
        font-weight: 800 !important;
        font-size: 1.6rem !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #008751 0%, #ffffff 100%);
        padding: 1.5rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        border: 3px solid #008751;
        font-weight: 700 !important;
    }
    .alert-box {
        background-color: #fff3cd;
        border: 3px solid #ffc107;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    .success-box {
        background-color: #d4edda;
        border: 3px solid #28a745;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    .warning-box {
        background-color: #f8d7da;
        border: 3px solid #dc3545;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        font-size: 1.2rem !important;
        font-weight: 700 !important;
    }
    .filter-section {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 12px;
        border-left: 6px solid #008751;
        margin: 15px 0;
    }
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 30px;
        margin-bottom: 25px;
    }
    .stMetric {
        font-size: 1.4rem !important;
        font-weight: 700 !important;
    }
    .stMarkdown h3 {
        font-size: 1.8rem !important;
        font-weight: 800 !important;
    }
    .stMarkdown h2 {
        font-size: 2.2rem !important;
        font-weight: 900 !important;
    }
    .stMarkdown h1 {
        font-size: 3rem !important;
        font-weight: 900 !important;
    }
    .stSelectbox label, .stRadio label, .stFileUploader label {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }
    .stButton button {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
        padding: 12px 24px;
    }
    .stExpander summary {
        font-size: 1.3rem !important;
        font-weight: 700 !important;
    }
    .multiselect-info {
        background-color: #e7f3ff;
        border: 1px solid #008751;
        border-radius: 5px;
        padding: 8px;
        margin: 5px 0;
        font-size: 0.9rem;
        color: #008751;
    }
</style>
""", unsafe_allow_html=True)

class PMTCTDashboard:
    def __init__(self, data):
        self.data = data
        self.clean_data()
    
    def clean_data(self):
        """Clean and preprocess the data"""
        # Replace empty strings with NaN
        self.data = self.data.replace('', np.nan)
        
        # Convert all columns to numeric where possible
        for col in self.data.columns:
            if col not in ['periodname', 'orgunitlevel1', 'orgunitlevel2', 'orgunitlevel3', 
                          'organisationunitname', 'organisationunitcode', 'perioddescription',
                          'periodid', 'periodcode']:
                self.data[col] = pd.to_numeric(self.data[col], errors='coerce').fillna(0)
    
    def safe_sum(self, column_name):
        """Safely sum a column, returning 0 if column doesn't exist"""
        if column_name in self.data.columns:
            return self.data[column_name].sum()
        return 0
    
    def calculate_percentage(self, numerator, denominator):
        """Calculate percentage safely"""
        if denominator > 0:
            return (numerator / denominator) * 100
        return 0
    
    def create_comparison_chart(self, title, numerator_col, denominator_col, numerator_label, denominator_label):
        """Create a comparison chart with percentage calculation"""
        numerator = self.safe_sum(numerator_col)
        denominator = self.safe_sum(denominator_col)
        percentage = self.calculate_percentage(numerator, denominator)
        
        fig = go.Figure()
        
        # Add bars
        fig.add_trace(go.Bar(
            x=[denominator_label, numerator_label],
            y=[denominator, numerator],
            marker_color=['#008751', '#87CEEB'],
            text=[f'{denominator:,}', f'{numerator:,}'],
            textposition='auto',
            textfont=dict(size=24, color='black', family="Arial Black")  # Much larger text in charts
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>{title}</b><br><sub>Coverage: {percentage:.1f}%</sub>",
                font=dict(size=26, color='black', family="Arial Black")  # Larger chart titles
            ),
            showlegend=False,
            height=500,
            font=dict(size=18, family="Arial"),  # Larger axis labels
            xaxis=dict(
                tickfont=dict(size=18, family="Arial Black"),  # Larger x-axis labels
                title_font=dict(size=20, family="Arial Black")  # Larger x-axis title
            ),
            yaxis=dict(
                tickfont=dict(size=18, family="Arial Black"),  # Larger y-axis labels
                title_font=dict(size=20, family="Arial Black")  # Larger y-axis title
            )
        )
        
        return fig, percentage, numerator, denominator
    
    def create_anc_hiv_testing_chart(self):
        """Create ANC HIV testing coverage chart"""
        anc_clients = self.safe_sum('PMTCT_ANC_1 Number of New ANC clients')
        hiv_tested_anc = self.safe_sum('PMTCT_HTS_6 Number of  pregnant women HIV tested and received results ANC')
        testing_rate = self.calculate_percentage(hiv_tested_anc, anc_clients)
        
        fig = go.Figure()
        
        categories = ['ANC Clients', 'HIV Tested (ANC)']
        values = [anc_clients, hiv_tested_anc]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#008751', '#87CEEB'],
            text=[f'{anc_clients:,}', f'{hiv_tested_anc:,}'],
            textposition='auto',
            textfont=dict(size=24, color='black', family="Arial Black")
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>ANC HIV Testing Coverage</b><br><sub>Testing Rate: {testing_rate:.1f}%</sub>",
                font=dict(size=26, color='black', family="Arial Black")
            ),
            height=500,
            showlegend=False,
            font=dict(size=18, family="Arial"),
            xaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            ),
            yaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            )
        )
        
        return fig, testing_rate
    
    def create_anc_treatment_cascade(self):
        """Create ANC treatment cascade"""
        hiv_positive_anc = self.safe_sum('PMTCT_HTS_7. Number of pregnant women tested HIV positive_ ANC')
        art_early = self.safe_sum('PMTCT_ART_15b. Number of HIV positive pregnant women newly started on  ART during ANC  <36wks of pregnancy')
        art_late = self.safe_sum('PMTCT_ART_15c. Number of HIV positive pregnant women newly started on  ART during ANC >36wks of pregnancy')
        
        total_art_anc = art_early + art_late
        
        # Calculate percentages
        art_early_percentage = self.calculate_percentage(art_early, hiv_positive_anc)
        art_late_percentage = self.calculate_percentage(art_late, hiv_positive_anc)
        total_art_percentage = self.calculate_percentage(total_art_anc, hiv_positive_anc)
        
        fig = go.Figure()
        
        categories = ['HIV Positive (ANC)', 'ART <36wks', 'ART >36wks', 'Total ART']
        values = [hiv_positive_anc, art_early, art_late, total_art_anc]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#008751', '#28a745', '#ffc107', '#dc3545'],
            text=[f'{val:,}' for val in values],
            textposition='auto',
            textfont=dict(size=22, color='black', family="Arial Black")
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>ANC Treatment Cascade</b><br><sub>Total ART Coverage: {total_art_percentage:.1f}%</sub>",
                font=dict(size=26, color='black', family="Arial Black")
            ),
            height=500,
            showlegend=False,
            font=dict(size=18, family="Arial"),
            xaxis=dict(
                tickfont=dict(size=18, family="Arial Black"),
                title_font=dict(size=20, family="Arial Black")
            ),
            yaxis=dict(
                tickfont=dict(size=18, family="Arial Black"),
                title_font=dict(size=20, family="Arial Black")
            )
        )
        
        return fig, total_art_percentage, art_early_percentage, art_late_percentage
    
    def create_ld_cascade(self):
        """Create Labour & Delivery cascade"""
        hiv_tested_ld = self.safe_sum('PMTCT_HTS_6 Number of  pregnant women HIV tested and received results L&D')
        hiv_positive_ld = self.safe_sum('PMTCT_HTS_7. Number of pregnant women tested HIV positive_ L&D')
        art_ld = self.safe_sum('PMTCT_ART_15d. Number of HIV positive pregnant women newly started on  ART during Labour')
        
        positivity_rate_ld = self.calculate_percentage(hiv_positive_ld, hiv_tested_ld) if hiv_tested_ld > 0 else 0
        art_coverage_ld = self.calculate_percentage(art_ld, hiv_positive_ld) if hiv_positive_ld > 0 else 0
        
        fig = go.Figure()
        
        categories = ['L&D Tested', 'L&D Positive', 'L&D ART']
        values = [hiv_tested_ld, hiv_positive_ld, art_ld]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#008751', '#ffc107', '#dc3545'],
            text=[f'{val:,}' for val in values],
            textposition='auto',
            textfont=dict(size=24, color='black', family="Arial Black")
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>Labour & Delivery Cascade</b><br><sub>Positivity: {positivity_rate_ld:.1f}% | ART Coverage: {art_coverage_ld:.1f}%</sub>",
                font=dict(size=26, color='black', family="Arial Black")
            ),
            height=500,
            showlegend=False,
            font=dict(size=18, family="Arial"),
            xaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            ),
            yaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            )
        )
        
        return fig, positivity_rate_ld, art_coverage_ld
    
    def create_previously_known_chart(self):
        """Create previously known HIV positive chart"""
        known_positive = self.safe_sum('PMTCT_HTS_5. Number of pregnant women with previously known HIV positive infection')
        already_on_art = self.safe_sum('PMTCT_ART_15a. Number of HIV positive pregnant women already on ART prior to this pregnancy')
        
        art_coverage_known = self.calculate_percentage(already_on_art, known_positive) if known_positive > 0 else 0
        
        fig = go.Figure()
        
        categories = ['Previously Known HIV+', 'Already on ART']
        values = [known_positive, already_on_art]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#008751', '#28a745'],
            text=[f'{val:,}' for val in values],
            textposition='auto',
            textfont=dict(size=24, color='black', family="Arial Black")
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>Previously Known HIV+ Women</b><br><sub>ART Coverage: {art_coverage_known:.1f}%</sub>",
                font=dict(size=26, color='black', family="Arial Black")
            ),
            height=500,
            showlegend=False,
            font=dict(size=18, family="Arial"),
            xaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            ),
            yaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            )
        )
        
        return fig, art_coverage_known
    
    def create_hub_spoke_referral(self):
        """Create hub and spoke referral chart"""
        referred = self.safe_sum('PMTCT_ART_15h. Number of Pregnant women referred to a Hub facility for treatment')
        initiated = self.safe_sum('PMTCT_ADDENDUM_15h Number of HIV positive pregnant women  identified in the spoke site who were initiated on ART in the comprehensive site')
        
        completion_rate = self.calculate_percentage(initiated, referred) if referred > 0 else 0
        
        fig = go.Figure()
        
        categories = ['Referred to Hub', 'Initiated at Hub']
        values = [referred, initiated]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#008751', '#87CEEB'],
            text=[f'{val:,}' for val in values],
            textposition='auto',
            textfont=dict(size=24, color='black', family="Arial Black")
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>Hub & Spoke Referral System</b><br><sub>Completion Rate: {completion_rate:.1f}%</sub>",
                font=dict(size=26, color='black', family="Arial Black")
            ),
            height=500,
            showlegend=False,
            font=dict(size=18, family="Arial"),
            xaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            ),
            yaxis=dict(
                tickfont=dict(size=20, family="Arial Black"),
                title_font=dict(size=22, family="Arial Black")
            )
        )
        
        return fig, completion_rate
    
    def create_eid_chart(self):
        """Create EID results chart"""
        samples_taken = self.safe_sum('PMTCT_EID_33. No. of of HEI whose samples were taken within 2 months of birth for DNA PCR')
        negative_results = self.safe_sum('PMTCT_EID_33. No. of HIV PCR results received for babies whose samples were taken for DNA PCR_Negative')
        positive_results = self.safe_sum('PMTCT_EID_33. No. of HIV PCR results received for babies whose samples were taken for DNA PCR_Positive')
        
        total_results = negative_results + positive_results
        result_coverage = self.calculate_percentage(total_results, samples_taken)
        positivity_rate = self.calculate_percentage(positive_results, total_results) if total_results > 0 else 0
        
        fig = go.Figure()
        
        categories = ['Samples Taken', 'Results Received', 'Negative', 'Positive']
        values = [samples_taken, total_results, negative_results, positive_results]
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#008751', '#87CEEB', '#28a745', '#dc3545'],
            text=[f'{val:,}' for val in values],
            textposition='auto',
            textfont=dict(size=22, color='black', family="Arial Black")
        ))
        
        fig.update_layout(
            title=dict(
                text=f"<b>EID Cascade</b><br><sub>Result Coverage: {result_coverage:.1f}% | Positivity: {positivity_rate:.1f}%</sub>",
                font=dict(size=26, color='black', family="Arial Black")
            ),
            height=500,
            showlegend=False,
            font=dict(size=18, family="Arial"),
            xaxis=dict(
                tickfont=dict(size=18, family="Arial Black"),
                title_font=dict(size=20, family="Arial Black")
            ),
            yaxis=dict(
                tickfont=dict(size=18, family="Arial Black"),
                title_font=dict(size=20, family="Arial Black")
            )
        )
        
        return fig, result_coverage, positivity_rate
    
    def create_comprehensive_art_chart(self):
        """Create comprehensive ART chart including postpartum"""
        art_early = self.safe_sum('PMTCT_ART_15b. Number of HIV positive pregnant women newly started on  ART during ANC  <36wks of pregnancy')
        art_late = self.safe_sum('PMTCT_ART_15c. Number of HIV positive pregnant women newly started on  ART during ANC >36wks of pregnancy')
        art_labour = self.safe_sum('PMTCT_ART_15d. Number of HIV positive pregnant women newly started on  ART during Labour')
        art_postpartum = self.safe_sum('PMTCT_ART_15e. Number of HIV positive pregnant women newly started on  ART during Post Partum (<72 hrs)')
        art_already = self.safe_sum('PMTCT_ART_15a. Number of HIV positive pregnant women already on ART prior to this pregnancy')
        
        total_new_art = art_early + art_late + art_labour + art_postpartum
        total_art = total_new_art + art_already
        
        categories = ['Already on ART', 'ART <36wks', 'ART >36wks', 'ART Labour', 'ART Postpartum', 'Total New ART', 'Total ART']
        values = [art_already, art_early, art_late, art_labour, art_postpartum, total_new_art, total_art]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=categories,
            y=values,
            marker_color=['#008751', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#17a2b8', '#20c997'],
            text=[f'{val:,}' for val in values],
            textposition='auto',
            textfont=dict(size=20, color='black', family="Arial Black")
        ))
        
        fig.update_layout(
            title=dict(
                text="<b>Comprehensive ART Initiation</b><br><sub>All Treatment Categories</sub>",
                font=dict(size=26, color='black', family="Arial Black")
            ),
            height=500,
            showlegend=False,
            font=dict(size=18, family="Arial"),
            xaxis=dict(
                tickfont=dict(size=16, family="Arial Black"),
                title_font=dict(size=18, family="Arial Black")
            ),
            yaxis=dict(
                tickfont=dict(size=16, family="Arial Black"),
                title_font=dict(size=18, family="Arial Black")
            )
        )
        
        return fig
    
    def create_reporting_trend(self):
        """Create reporting rate trend chart"""
        if 'periodname' in self.data.columns:
            reporting_data = self.data.groupby('periodname').agg({
                'PMTCT MSF Comprehensive - Reporting rate': 'mean',
                'PMTCT MSF FOR SPOKE SITES   - Reporting rate': 'mean'
            }).reset_index()
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=reporting_data['periodname'],
                y=reporting_data['PMTCT MSF Comprehensive - Reporting rate'],
                mode='lines+markers',
                name='Comprehensive Sites',
                line=dict(color='#008751', width=4)
            ))
            
            fig.add_trace(go.Scatter(
                x=reporting_data['periodname'],
                y=reporting_data['PMTCT MSF FOR SPOKE SITES   - Reporting rate'],
                mode='lines+markers',
                name='Spoke Sites',
                line=dict(color='#FFD700', width=4)
            ))
            
            # Add 90% threshold line
            fig.add_hline(y=90, line_dash="dash", line_color="red", annotation_text="90% Target")
            
            fig.update_layout(
                title=dict(
                    text="<b>Reporting Rate Trends</b>",
                    font=dict(size=26, color='black', family="Arial Black")
                ),
                xaxis_title="Period",
                yaxis_title="Reporting Rate (%)",
                height=500,
                font=dict(size=18, family="Arial"),
                legend=dict(font=dict(size=16, family="Arial Black")),
                xaxis=dict(
                    tickfont=dict(size=16, family="Arial Black"),
                    title_font=dict(size=18, family="Arial Black")
                ),
                yaxis=dict(
                    tickfont=dict(size=16, family="Arial Black"),
                    title_font=dict(size=18, family="Arial Black")
                )
            )
            
            return fig
        return None

def get_quarter_from_month(month_name):
    """Convert month name to quarter"""
    month_to_quarter = {
        'January': 'Quarter 1', 'February': 'Quarter 1', 'March': 'Quarter 1',
        'April': 'Quarter 2', 'May': 'Quarter 2', 'June': 'Quarter 2',
        'July': 'Quarter 3', 'August': 'Quarter 3', 'September': 'Quarter 3',
        'October': 'Quarter 4', 'November': 'Quarter 4', 'December': 'Quarter 4'
    }
    return month_to_quarter.get(month_name, 'Unknown Quarter')

def extract_year_from_period(period_name):
    """Extract year from period name"""
    # Handle different period formats
    if isinstance(period_name, str):
        # Look for 4-digit years
        import re
        year_match = re.search(r'20\d{2}', period_name)
        if year_match:
            return year_match.group()
    return 'Unknown Year'

def main():
    # Header with Nigerian theme and logos
    st.markdown("""
    <div class="logo-container">
        <!-- Add your Nigerian coat of arms and Global Fund logos here -->
        <h1 class="main-header">🇳🇬 PMTCT DASHBOARD - NIGERIA</h1>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### Prevention of Mother-to-Child Transmission Program")
    st.markdown("---")
    
    # File upload
    st.sidebar.markdown("### 📁 DATA UPLOAD")
    uploaded_file = st.sidebar.file_uploader("Upload PMTCT Data CSV File", type=['csv'])
    
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.sidebar.success(f"✅ Data loaded successfully: {len(df)} records")
        
        # Show available columns for verification
        with st.sidebar.expander("🔍 Verify Columns"):
            st.write("Columns found:", len(df.columns))
            st.write(list(df.columns))
    else:
        st.warning("⚠️ Please upload a CSV file to populate the dashboard")
        st.stop()
    
    dashboard = PMTCTDashboard(df)
    
    # FILTERS SECTION
    st.sidebar.markdown("### 🔍 FILTERS")
    
    # Period filter with clear headings
    st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.sidebar.markdown("**📅 TIME PERIOD FILTER**")
    
    if 'periodname' in df.columns:
        # Extract unique periods and sort them
        all_periods = sorted(list(df['periodname'].unique()))
        
        # Add quarter and year information to the data
        df['quarter'] = df['periodname'].apply(get_quarter_from_month)
        df['year'] = df['periodname'].apply(extract_year_from_period)
        
        # Get unique quarters and years
        unique_quarters = sorted(list(df['quarter'].unique()))
        unique_years = sorted(list(df['year'].unique()))
        
        # Quarter filter
        selected_quarters = st.sidebar.multiselect(
            "Select Quarter(s)", 
            unique_quarters,
            default=unique_quarters,
            help="Select one or multiple quarters to analyze"
        )
        
        # Year filter
        selected_years = st.sidebar.multiselect(
            "Select Year(s)",
            unique_years,
            default=unique_years,
            help="Select one or multiple years to analyze"
        )
        
        # Month filter (filtered by selected quarters and years)
        if selected_quarters and selected_years:
            # Filter months based on selected quarters and years
            filtered_months = []
            for period in all_periods:
                quarter = get_quarter_from_month(period)
                year = extract_year_from_period(period)
                if quarter in selected_quarters and year in selected_years:
                    filtered_months.append(period)
        else:
            filtered_months = all_periods
        
        selected_months = st.sidebar.multiselect(
            "Select Month(s)",
            filtered_months,
            default=filtered_months,
            help="Select one or multiple months to analyze"
        )
        
        # Show selection info
        if selected_quarters:
            st.sidebar.markdown(f'<div class="multiselect-info">📊 Selected: {len(selected_quarters)} quarter(s)</div>', unsafe_allow_html=True)
        if selected_years:
            st.sidebar.markdown(f'<div class="multiselect-info">📅 Selected: {len(selected_years)} year(s)</div>', unsafe_allow_html=True)
        if selected_months:
            st.sidebar.markdown(f'<div class="multiselect-info">📈 Selected: {len(selected_months)} month(s)</div>', unsafe_allow_html=True)
    
    else:
        selected_quarters = []
        selected_years = []
        selected_months = []
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Geographical filters with clear headings
    st.sidebar.markdown('<div class="filter-section">', unsafe_allow_html=True)
    st.sidebar.markdown("**🗺️ GEOGRAPHICAL FILTERS**")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if 'orgunitlevel1' in df.columns:
            states = sorted(list(df['orgunitlevel1'].unique()))
            selected_states = st.multiselect(
                "Select State(s)", 
                states,
                default=states,
                help="Select one or multiple states"
            )
            
            if selected_states:
                st.markdown(f'<div class="multiselect-info">📍 Selected: {len(selected_states)} state(s)</div>', unsafe_allow_html=True)
        else:
            selected_states = []
    
    with col2:
        if 'orgunitlevel2' in df.columns:
            lgas = sorted(list(df['orgunitlevel2'].unique()))
            selected_lgas = st.multiselect(
                "Select LGA(s)", 
                lgas,
                default=lgas,
                help="Select one or multiple LGAs"
            )
            
            if selected_lgas:
                st.markdown(f'<div class="multiselect-info">🏙️ Selected: {len(selected_lgas)} LGA(s)</div>', unsafe_allow_html=True)
        else:
            selected_lgas = []
    
    if 'orgunitlevel3' in df.columns:
        facilities = sorted(list(df['orgunitlevel3'].unique()))
        selected_facilities = st.sidebar.multiselect(
            "Select Health Facility(s)", 
            facilities,
            default=facilities,
            help="Select one or multiple health facilities"
        )
        
        if selected_facilities:
            st.sidebar.markdown(f'<div class="multiselect-info">🏥 Selected: {len(selected_facilities)} facility(s)</div>', unsafe_allow_html=True)
    else:
        selected_facilities = []
    
    st.sidebar.markdown('</div>', unsafe_allow_html=True)
    
    # Apply filters
    filtered_df = df.copy()
    
    # Apply time period filters
    if selected_months:
        filtered_df = filtered_df[filtered_df['periodname'].isin(selected_months)]
    
    # Apply geographical filters
    if selected_states:
        filtered_df = filtered_df[filtered_df['orgunitlevel1'].isin(selected_states)]
    
    if selected_lgas:
        filtered_df = filtered_df[filtered_df['orgunitlevel2'].isin(selected_lgas)]
    
    if selected_facilities:
        filtered_df = filtered_df[filtered_df['orgunitlevel3'].isin(selected_facilities)]
    
    # Clear filters button
    col1, col2 = st.sidebar.columns(2)
    with col1:
        if st.button("🔄 Clear Filters", use_container_width=True):
            st.rerun()
    
    with col2:
        if st.button("📊 Apply Filters", use_container_width=True):
            st.rerun()
    
    # Show filter summary
    if len(filtered_df) < len(df):
        st.sidebar.info(f"**Filter Summary:**\n- {len(filtered_df)} of {len(df)} records shown\n- {len(selected_quarters)} quarter(s)\n- {len(selected_years)} year(s)\n- {len(selected_months)} month(s)\n- {len(selected_states)} state(s)\n- {len(selected_lgas)} LGA(s)\n- {len(selected_facilities)} facility(s)")
    
    dashboard.data = filtered_df
    
    # KEY PERFORMANCE INDICATORS - COVERAGE PERCENTAGES
    st.markdown("---")
    st.markdown("### 📊 KEY PERFORMANCE INDICATORS (COVERAGE %)")
    
    # Calculate all coverage percentages
    anc_clients = dashboard.safe_sum('PMTCT_ANC_1 Number of New ANC clients')
    hiv_tested_anc = dashboard.safe_sum('PMTCT_HTS_6 Number of  pregnant women HIV tested and received results ANC')
    hiv_tested_ld = dashboard.safe_sum('PMTCT_HTS_6 Number of  pregnant women HIV tested and received results L&D')
    hbv_tested = dashboard.safe_sum('PMTCT_HTS_10. Number of new ANC Clients tested for HBV ( ANC, L&D, <72hrs Post Partum)')
    hcv_tested = dashboard.safe_sum('PMTCT_HTS_11. Number of new ANC Clients tested for HCV ( ANC, L&D, <72hrs Post Partum)')
    eid_samples = dashboard.safe_sum('PMTCT_EID_33. No. of of HEI whose samples were taken within 2 months of birth for DNA PCR')
    
    # Total HIV positive women (ANC + L&D + Previously known)
    hiv_positive_anc = dashboard.safe_sum('PMTCT_HTS_7. Number of pregnant women tested HIV positive_ ANC')
    hiv_positive_ld = dashboard.safe_sum('PMTCT_HTS_7. Number of pregnant women tested HIV positive_ L&D')
    previously_known = dashboard.safe_sum('PMTCT_HTS_5. Number of pregnant women with previously known HIV positive infection')
    total_hiv_positive = hiv_positive_anc + hiv_positive_ld + previously_known
    
    # Calculate coverage percentages
    anc_testing_coverage = dashboard.calculate_percentage(hiv_tested_anc, anc_clients)
    ld_testing_coverage = dashboard.calculate_percentage(hiv_tested_ld, anc_clients)
    hbv_testing_coverage = dashboard.calculate_percentage(hbv_tested, anc_clients)
    hcv_testing_coverage = dashboard.calculate_percentage(hcv_tested, anc_clients)
    eid_coverage = dashboard.calculate_percentage(eid_samples, total_hiv_positive) if total_hiv_positive > 0 else 0
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("ANC HIV Testing", f"{anc_testing_coverage:.1f}%")
    
    with col2:
        st.metric("L&D HIV Testing", f"{ld_testing_coverage:.1f}%")
    
    with col3:
        st.metric("HBV Testing", f"{hbv_testing_coverage:.1f}%")
    
    with col4:
        st.metric("HCV Testing", f"{hcv_testing_coverage:.1f}%")
    
    with col5:
        st.metric("EID Coverage", f"{eid_coverage:.1f}%")
    
    # VISUALIZATION SECTION 1: ANC HIV Testing
    st.markdown("---")
    st.markdown('<div class="section-header">NEW ANC VISIT VS HIV TESTING</div>', unsafe_allow_html=True)
    
    fig_anc_testing, testing_rate = dashboard.create_anc_hiv_testing_chart()
    st.plotly_chart(fig_anc_testing, use_container_width=True)
    
    # Feedback for ANC testing
    if testing_rate >= 90:
        st.markdown(f'<div class="success-box">✅ Excellent! ANC HIV testing coverage is {testing_rate:.1f}% (≥90%)</div>', unsafe_allow_html=True)
    elif testing_rate >= 70:
        st.markdown(f'<div class="alert-box">⚠️ Moderate: ANC HIV testing coverage is {testing_rate:.1f}% (70-89%)</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="warning-box">❌ Critical: ANC HIV testing coverage is {testing_rate:.1f}% (<70%)</div>', unsafe_allow_html=True)
    
    # VISUALIZATION SECTION 2: ANC Treatment Cascade
    st.markdown("---")
    st.markdown('<div class="section-header">TESTED POSITIVE VERSUS STARTED ON TREATMENT ANC</div>', unsafe_allow_html=True)
    
    fig_anc_treatment, total_art_percentage, art_early_percentage, art_late_percentage = dashboard.create_anc_treatment_cascade()
    st.plotly_chart(fig_anc_treatment, use_container_width=True)
    
    # Feedback for ANC treatment
    col1, col2 = st.columns(2)
    with col1:
        if art_early_percentage >= 80:
            st.markdown(f'<div class="success-box">✅ Early ART (<36wks): {art_early_percentage:.1f}%</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">❌ Early ART (<36wks): {art_early_percentage:.1f}%</div>', unsafe_allow_html=True)
    
    with col2:
        if total_art_percentage >= 90:
            st.markdown(f'<div class="success-box">✅ Total ART Coverage: {total_art_percentage:.1f}%</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="warning-box">❌ Total ART Coverage: {total_art_percentage:.1f}%</div>', unsafe_allow_html=True)
    
    # VISUALIZATION SECTION 3: Labour & Delivery and Previously Known
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">LABOUR AND DELIVERY POSITIVE VERSUS TREATMENT</div>', unsafe_allow_html=True)
        fig_ld_cascade, positivity_rate_ld, art_coverage_ld = dashboard.create_ld_cascade()
        st.plotly_chart(fig_ld_cascade, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">PREVIOUSLY KNOWN ON ART</div>', unsafe_allow_html=True)
        fig_known, art_coverage_known = dashboard.create_previously_known_chart()
        st.plotly_chart(fig_known, use_container_width=True)
    
    # VISUALIZATION SECTION 4: Comprehensive ART Overview
    st.markdown("---")
    st.markdown('<div class="section-header">COMPREHENSIVE ART INITIATION OVERVIEW</div>', unsafe_allow_html=True)
    
    fig_comprehensive_art = dashboard.create_comprehensive_art_chart()
    st.plotly_chart(fig_comprehensive_art, use_container_width=True)
    
    # VISUALIZATION SECTION 5: Viral Hepatitis Testing
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">VIRAL HEPATITIS TESTING B (HBV)</div>', unsafe_allow_html=True)
        fig_hbv, hbv_percentage, hbv_tested, anc_clients = dashboard.create_comparison_chart(
            "HBV Testing Coverage",
            'PMTCT_HTS_10. Number of new ANC Clients tested for HBV ( ANC, L&D, <72hrs Post Partum)',
            'PMTCT_ANC_1 Number of New ANC clients',
            "HBV Tested", "ANC Clients"
        )
        st.plotly_chart(fig_hbv, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">VIRAL HEPATITIS TESTING C (HCV)</div>', unsafe_allow_html=True)
        fig_hcv, hcv_percentage, hcv_tested, anc_clients = dashboard.create_comparison_chart(
            "HCV Testing Coverage",
            'PMTCT_HTS_11. Number of new ANC Clients tested for HCV ( ANC, L&D, <72hrs Post Partum)',
            'PMTCT_ANC_1 Number of New ANC clients',
            "HCV Tested", "ANC Clients"
        )
        st.plotly_chart(fig_hcv, use_container_width=True)
    
    # VISUALIZATION SECTION 6: Syphilis Testing and Treatment
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">SYPHILLIS TESTING</div>', unsafe_allow_html=True)
        fig_syphilis_test, syphilis_test_percentage, syphilis_tested, anc_clients = dashboard.create_comparison_chart(
            "Syphilis Testing Coverage",
            'PMTCT_ANC_2. Number of new ANC Clients tested for syphilis total',
            'PMTCT_ANC_1 Number of New ANC clients',
            "Syphilis Tested", "ANC Clients"
        )
        st.plotly_chart(fig_syphilis_test, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">SYPHILLIS TREATMENT</div>', unsafe_allow_html=True)
        fig_syphilis_treat, syphilis_treat_percentage, syphilis_treated, syphilis_positive = dashboard.create_comparison_chart(
            "Syphilis Treatment Coverage",
            'PMTCT_ANC_4. Number of the ANC Clients treated for Syphilis total',
            'PMTCT_ANC_3. Number of new ANC Clients tested positive for syphilis Total',
            "Treated", "Syphilis Positive"
        )
        st.plotly_chart(fig_syphilis_treat, use_container_width=True)
    
    # VISUALIZATION SECTION 7: Delivery Cascade and EID
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">DELIVERY CASCADE</div>', unsafe_allow_html=True)
        fig_delivery, delivery_percentage, hiv_deliveries, total_deliveries = dashboard.create_comparison_chart(
            "Delivery Coverage for HIV+ Women",
            'PMTCT_L&D_21. Number of booked HIV positive pregnant women who delivered at facility',
            'PMTCT_L&D_20. Total deliveries at facility (booked and unbooked pregnant women)',
            "HIV+ Deliveries", "Total Deliveries"
        )
        st.plotly_chart(fig_delivery, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">EID SAMPLE COLLECTION & RESULTS</div>', unsafe_allow_html=True)
        fig_eid, eid_coverage, eid_positivity = dashboard.create_eid_chart()
        st.plotly_chart(fig_eid, use_container_width=True)
    
    # VISUALIZATION SECTION 8: Hub & Spoke and Reporting Rates
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="section-header">HUB & SPOKE REFERRAL SYSTEM</div>', unsafe_allow_html=True)
        fig_referral, completion_rate = dashboard.create_hub_spoke_referral()
        st.plotly_chart(fig_referral, use_container_width=True)
    
    with col2:
        st.markdown('<div class="section-header">REPORTING RATE TRENDS</div>', unsafe_allow_html=True)
        fig_reporting = dashboard.create_reporting_trend()
        if fig_reporting:
            st.plotly_chart(fig_reporting, use_container_width=True)
            
            # Check reporting rates
            comp_rate = dashboard.data['PMTCT MSF Comprehensive - Reporting rate'].mean()
            spoke_rate = dashboard.data['PMTCT MSF FOR SPOKE SITES   - Reporting rate'].mean()
            
            col1, col2 = st.columns(2)
            with col1:
                if comp_rate >= 90:
                    st.markdown(f'<div class="success-box">✅ Comprehensive Sites: {comp_rate:.1f}%</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="warning-box">❌ Comprehensive Sites: {comp_rate:.1f}%</div>', unsafe_allow_html=True)
            
            with col2:
                if spoke_rate >= 90:
                    st.markdown(f'<div class="success-box">✅ Spoke Sites: {spoke_rate:.1f}%</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="warning-box">❌ Spoke Sites: {spoke_rate:.1f}%</div>', unsafe_allow_html=True)
        else:
            st.info("No period data available for trend analysis")
    
    # Data Summary and Export
    st.markdown("---")
    st.markdown("### 📋 DATA SUMMARY & EXPORT")
    
    # Show summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Facilities", len(filtered_df))
        st.metric("Total ANC Clients", f"{anc_clients:,}")
    
    with col2:
        st.metric("Total HIV+ Women", total_hiv_positive)
        st.metric("Total Deliveries", f"{total_deliveries:,}")
    
    with col3:
        st.metric("EID Samples", eid_samples)
        st.metric("Filtered Records", len(filtered_df))
    
    csv = filtered_df.to_csv(index=False)
    st.download_button(
        label="📥 Download Filtered Data as CSV",
        data=csv,
        file_name="pmtct_filtered_data.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()