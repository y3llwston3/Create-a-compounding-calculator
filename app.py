from flask import Flask, render_template, request
import io
import base64
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            # Extract form data with default values
            initial_deposit = float(request.form.get('initial_deposit', 0))
            interest_rate = float(request.form.get('interest_rate', 0))
            contribution = float(request.form.get('contribution', 0))
            compounding_type = request.form.get('compounding_type', 'monthly')
            time_period_years = int(float(request.form.get('time_period_years', 0)))  # Ensure integer

            # Determine number of compounding periods per year
            n = 12 if compounding_type == 'monthly' else 1

            # Calculate total amount and contributions
            total_amount = initial_deposit * (1 + interest_rate / n) ** (n * time_period_years)
            total_contributions = contribution * (((1 + interest_rate / n) ** (n * time_period_years) - 1) / (interest_rate / n))
            final_amount_with_interest = total_amount + total_contributions

            # Calculate contributions without interest
            total_contributions_without_interest = initial_deposit + contribution * time_period_years * n
            difference = final_amount_with_interest - total_contributions_without_interest

            # Prepare data for plotting
            amounts_with_interest = []
            amounts_without_interest = []
            years = list(range(time_period_years + 1))

            for year in years:
                year_total_amount = initial_deposit * (1 + interest_rate / n) ** (n * year)
                year_total_contributions = contribution * (((1 + interest_rate / n) ** (n * year) - 1) / (interest_rate / n))
                year_total_contributions_without_interest = initial_deposit + contribution * year * n

                amounts_with_interest.append(year_total_amount + year_total_contributions)
                amounts_without_interest.append(year_total_contributions_without_interest)

            # Plot results
            plt.figure(figsize=(10, 5))
            plt.plot(years, amounts_with_interest, marker='o', label='With Interest')
            plt.plot(years, amounts_without_interest, marker='o', label='Without Interest')
            plt.title('Compound Interest Over Time Comparison')
            plt.xlabel('Years')
            plt.ylabel('Amount in Dollars')
            plt.grid(True)
            plt.legend()

            # Save plot to a BytesIO object
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url = base64.b64encode(img.getvalue()).decode()

            # Render the results template with calculated data
            return render_template('result.html', final_amount=final_amount_with_interest, difference=difference, plot_url=plot_url)

        except Exception as e:
            return f"An error occurred: {e}", 400

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
